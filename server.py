import os
import sys
import json
import httpx
from mcp.server.fastmcp import FastMCP

# 1. Initialize the MCP Server
mcp = FastMCP("ServiceNow Agent")

# --- LOGGER HELPER ---
def log(message):
    """Writes logs to stderr so they show up in the Claude logs without breaking the connection."""
    sys.stderr.write(f"[DEBUG] {message}\n")
    sys.stderr.flush()

# 2. Helper for API Requests
def make_request(method, endpoint, params=None, json_data=None):
    """Handles the actual HTTP call to ServiceNow"""
    instance = os.environ.get("SN_INSTANCE")
    user = os.environ.get("SN_USER")
    password = os.environ.get("SN_PASS")
    
    if not instance or not user or not password:
        log("❌ CRITICAL: Missing Environment Variables!")
        raise ValueError("Missing SN_INSTANCE, SN_USER, or SN_PASS environment variables.")

    url = f"{instance}/api/{endpoint}"
    auth = (user, password)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    log(f"📡 API CALL: {method} {url}")
    if params: log(f"   PARAMS: {params}")
    if json_data: log(f"   PAYLOAD: {json.dumps(json_data)}")

    with httpx.Client(timeout=15.0) as client:
        response = client.request(method, url, auth=auth, headers=headers, params=params, json=json_data)
        
        # Log failures
        if response.status_code >= 400:
            log(f"❌ ERROR {response.status_code}: {response.text}")
        
        if response.status_code == 404: 
            return None
            
        response.raise_for_status()
        return response.json()

# --- 3. DEFINE TOOLS ---

@mcp.tool()
def check_ticket_status(ticket_number: str) -> str:
    """Checks the status of an Incident (INC), Request (REQ), or Item (RITM)."""
    log(f"🔍 Tool called: check_ticket_status('{ticket_number}')")
    
    table = "incident"
    if ticket_number.startswith("RITM"): table = "sc_req_item"
    elif ticket_number.startswith("REQ"): table = "sc_request"
    
    params = {"sysparm_query": f"number={ticket_number}", "sysparm_fields": "state,short_description,number"}
    data = make_request("GET", f"now/table/{table}", params=params)
    
    if not data or not data['result']: 
        log("   Result: Ticket not found")
        return "Ticket not found."
        
    rec = data['result'][0]
    result_str = f"{rec['number']}: {rec['short_description']} (State: {rec['state']})"
    log(f"   ✅ Success: {result_str}")
    return result_str

@mcp.tool()
def search_knowledge_base(query: str) -> str:
    """Searches for 'how to' articles in the Knowledge Base."""
    log(f"📚 Tool called: search_knowledge_base('{query}')")
    
    params = {
        "sysparm_query": f"short_descriptionLIKE{query}^workflow_state=published",
        "sysparm_fields": "number,short_description,text",
        "sysparm_limit": 3
    }
    data = make_request("GET", "now/table/kb_knowledge", params=params)
    
    if not data or not data['result']: return "No articles found."
    
    output = ""
    for art in data['result']:
        text = art['text'].replace("<p>", "").replace("</p>", "")[:200]
        output += f"### {art['number']}: {art['short_description']}\n{text}...\n\n"
    return output

@mcp.tool()
def get_catalog_variables(item_name: str) -> str:
    """Inspects a Catalog Item to find required variables before ordering."""
    log(f"🧐 Tool called: get_catalog_variables('{item_name}')")
    
    # Find Item
    params = {"sysparm_query": f"name={item_name}", "sysparm_limit": 1}
    data = make_request("GET", "now/table/sc_cat_item", params=params)
    if not data or not data['result']: 
        log(f"   ❌ Item '{item_name}' not found")
        return f"Item '{item_name}' not found."
    
    item = data['result'][0]
    log(f"   Found Item: {item['name']} (ID: {item['sys_id']})")
    
    # Get Variables
    v_params = {"sysparm_query": f"cat_item={item['sys_id']}^active=true", "sysparm_fields": "question_text,name,mandatory"}
    v_data = make_request("GET", "now/table/item_option_new", params=v_params)
    
    output = f"ITEM: {item['name']}\nVARIABLES:\n"
    for v in v_data['result']:
        mand = "[MANDATORY]" if v['mandatory'] == 'true' else "(Optional)"
        line = f"- {v['question_text']} (Key: {v['name']}) {mand}"
        output += line + "\n"
        log(f"   Found Var: {line}") # Log each variable found
        
    return output

@mcp.tool()
def get_user_id(name_or_email: str) -> str:
    """Finds a user's sys_id by their name or email."""
    log(f"👤 Tool called: get_user_id('{name_or_email}')")

    query = f"nameLIKE{name_or_email}^ORemailLIKE{name_or_email}^active=true"
    params = {
        "sysparm_query": query,
        "sysparm_fields": "sys_id,name,email,user_name",
        "sysparm_limit": 5
    }
    
    data = make_request("GET", "now/table/sys_user", params=params)
    
    if not data or not data['result']: 
        return f"User '{name_or_email}' not found."
    
    output = "Found Users:\n"
    for u in data['result']:
        info = f"- Name: {u['name']} | Email: {u['email']} | UserID: {u['user_name']} | SYS_ID: {u['sys_id']}"
        output += info + "\n"
        log(f"   {info}")
        
    return output

@mcp.tool()
def submit_catalog_request(item_name: str, variables_json: str) -> str:
    """Orders a Catalog Item. 'variables_json' must be valid JSON."""
    log(f"🛒 Tool called: submit_catalog_request('{item_name}')")
    log(f"   Input Variables: {variables_json}")

    try:
        vars_dict = json.loads(variables_json)
    except:
        log("   ❌ Error: Invalid JSON format")
        return "Error: variables_json must be valid JSON."

    # Get Item ID
    params = {"sysparm_query": f"name={item_name}", "sysparm_limit": 1}
    data = make_request("GET", "now/table/sc_cat_item", params=params)
    if not data or not data['result']: return "Item not found."
    sys_id = data['result'][0]['sys_id']
    
    # Submit Order
    # NEW (Correct)
    endpoint = f"sn_sc/servicecatalog/items/{sys_id}/order_now"
    payload = {"sysparm_quantity": "1", "variables": vars_dict}
    
    try:
        res = make_request("POST", endpoint, json_data=payload)
        result = res.get('result', {})
        req_num = result.get('request_number') or result.get('number')
        log(f"   ✅ SUCCESS: Created {req_num}")
        return f"SUCCESS! Request {req_num} created."
    except Exception as e:
        log(f"   ❌ FAILED: {str(e)}")
        return f"FAILED: {str(e)}"

if __name__ == "__main__":
    # Runs the server over Standard Input/Output (stdio)
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        log(f"🔥 FATAL ERROR: {e}")