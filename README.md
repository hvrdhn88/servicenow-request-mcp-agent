This is a local AI Agent that connects Claude Desktop directly to your ServiceNow instance.

Unlike a standard chatbot, this agent uses the Model Context Protocol (MCP) to give Claude "hands." It can inspect forms, look up user IDs, and submit live orders to your instance—all from your local machine.

📋 Prerequisites
Before you start, make sure you have:

Python 3.10+ installed on your computer.

The Claude Desktop App installed.

A ServiceNow Developer Instance (or any instance where you have API access).

🚀 Step 1: Download the Agent
Open your terminal and clone this repository:

Bash
git clone https://github.com/hvrdhn88/servicenow-request-mcp-agent.git
cd servicenow-mcp-agent
🛠️ Step 2: Set Up the Environment
We use a virtual environment to keep things clean. Run these commands:

Mac/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Windows:

Bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Note: The requirements.txt file installs the mcp and httpx libraries automatically.

⚙️ Step 3: Connect to Claude (The Important Part)
Claude needs to know two things:

Where your Python script is (server.py).

Your ServiceNow credentials (URL, Username, Password).

1. Open the Claude Config File:

Mac: ~/Library/Application Support/Claude/claude_desktop_config.json

Windows: %APPDATA%\Claude\claude_desktop_config.json

2. Add this configuration: (Replace the paths and credentials with YOUR actual values)

JSON
{
  "mcpServers": {
    "servicenow-agent": {
      "command": "/ABSOLUTE/PATH/TO/YOUR/REPO/venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/YOUR/REPO/server.py"
      ],
      "env": {
        "SN_INSTANCE": "https://devXXXXX.service-now.com",
        "SN_USER": "admin",
        "SN_PASS": "YOUR_REAL_PASSWORD"
      }
    }
  }
}

⚠️ Crucial Tip: You must use the Absolute Path.

Wrong: venv/bin/python

Right: /Users/harshvardhan/Desktop/servicenow-mcp-agent/venv/bin/python

To find your path, type pwd in your terminal inside the folder.

🎮 Step 4: Run It!
Restart the Claude Desktop App completely.

Look for the 🔌 Plug Icon in the input bar. If it's there, you are connected!

Start chatting.

Try these prompts:
"Check the status of incident INC0010005." (The agent will fetch the live state and description).

"Search the Knowledge Base for 'email issues'." (It will summarize relevant articles).

"Order a 'Developer Laptop' for user 'Abraham Lincoln'." (The agent will inspect the form, find Abraham's sys_id, and submit the request).

❓ Troubleshooting
Q: Claude says "I don't have access to that tool." A: Check your claude_desktop_config.json. Did you restart Claude? Is the path to server.py correct?

Q: I get a "400 Bad Request" when ordering. A: This usually means the variable name is wrong. Ask Claude: "Check the variables for this item first, then tell me the internal keys."

Q: I get a "401 Unauthorized" error. A: Your password in the config file is wrong. Double-check your SN_PASS.

👨‍💻 Contributing
Feel free to open an issue or submit a Pull Request if you want to add more features (like Change Management or User Administration)!
