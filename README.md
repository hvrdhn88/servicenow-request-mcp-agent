Ahhh yep — I see exactly what happened 😅
The issue is **missing section breaks and code fences**, so Markdown thinks parts of Steps 2–4 are still inside the Step 1 code block.

Here’s a **fixed, GitHub-safe `README.md`** where **Steps 1–4 all render at the same heading level**, clean and aligned.

👉 **Copy-paste this entire block as-is**

---

````md
# 🤖 ServiceNow Request MCP Agent

**A local AI Agent that connects Claude Desktop directly to your ServiceNow instance.**

Unlike a standard chatbot, this agent uses the **Model Context Protocol (MCP)** to give Claude *hands*.  
It can inspect forms, look up user IDs, and submit live orders to your instance — all from your local machine.

---

## 📋 Prerequisites

Before you start, make sure you have:

1. **Python 3.10+** installed  
2. The **[Claude Desktop App](https://claude.ai/download)** installed  
3. A **ServiceNow Developer Instance** (or any instance with API access)

---

## 🚀 Step 1: Download the Agent

Open your terminal and clone this repository:

```bash
git clone https://github.com/hvrdhn88/servicenow-request-mcp-agent.git
cd servicenow-request-mcp-agent
````

---

## 🛠️ Step 2: Set Up the Environment

We use a virtual environment to keep things clean.

### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** The `requirements.txt` file installs `mcp` and `httpx` automatically.

---

## ⚙️ Step 3: Connect to Claude

You need to tell Claude where your MCP server script lives.

### Open the Claude config file

* **Mac:**
  `~/Library/Application Support/Claude/claude_desktop_config.json`

* **Windows:**
  `%APPDATA%\Claude\claude_desktop_config.json`

### Add this configuration (update the paths)

```json
{
  "mcpServers": {
    "servicenow-agent": {
      "command": "/ABSOLUTE/PATH/TO/YOUR/venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/YOUR/server.py"
      ],
      "env": {
        "SN_INSTANCE": "https://devXXXXX.service-now.com",
        "SN_USER": "admin",
        "SN_PASS": "YOUR_REAL_PASSWORD"
      }
    }
  }
}
```

⚠️ **Important**

* You must use **absolute paths**
* Relative paths like `venv/bin/python` **will not work**

---

## 🎮 Step 4: Run It!

1. Restart **Claude Desktop** completely
2. Look for the **🔌 Plug icon**
3. Start chatting!

### Example Prompts

```text
Check the status of incident INC0010005.
```

```text
Search the Knowledge Base for "email issues".
```

```text
Order a "Developer Laptop" for user "Abraham Lincoln".
```

---

## 🧠 What This Enables

* Live ServiceNow data access
* No custom REST scripts per table
* Dynamic discovery via MCP
* Secure, local-first execution

Perfect for **POCs, PDIs, and agent experimentation** 🚀

```

---

### Why this now works ✅
- Every code block is **explicitly closed**
- Each step has its own `##` heading
- No text accidentally lives inside a code fence
- GitHub Markdown renders **Step 1–4 at the same level**

If you want, I can also:
- Add a **Quick Start (TL;DR)** section
- Add **Troubleshooting (common MCP errors)**
- Add a **ServiceNow table coverage list**

Just tell me 👍
```
