# 🤖 ServiceNow Request MCP Agent

**A local AI Agent that connects Claude Desktop directly to your ServiceNow instance.**

Unlike a standard chatbot, this agent uses the **Model Context Protocol (MCP)** to give Claude "hands." It can inspect forms, look up user IDs, and submit live orders to your instance—all from your local machine.

---

## 📋 Prerequisites

Before you start, make sure you have:
1. **Python 3.10+** installed.
2. The **[Claude Desktop App](https://claude.ai/download)** installed.
3. A **ServiceNow Developer Instance** (or any instance with API access).

---

## 🚀 Step 1: Download the Agent

Open your terminal and clone this repository:

```bash
git clone https://github.com/hvrdhn88/servicenow-request-mcp-agent.git
cd servicenow-request-mcp-agent

🛠️ Step 2: Set Up the Environment
We use a virtual environment to keep things clean.

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
Note: The requirements.txt file installs mcp and httpx automatically.

⚙️ Step 3: Connect to Claude
You need to tell Claude where your script is.

Open the config file:

Mac: ~/Library/Application Support/Claude/claude_desktop_config.json

Windows: %APPDATA%\Claude\claude_desktop_config.json

Add this configuration (Update the paths!):

JSON
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
🎮 Step 4: Run It!
Restart Claude Desktop completely.

Look for the 🔌 Plug Icon.

Start chatting!

Example Prompts:

"Check the status of incident INC0010005."

"Search the Knowledge Base for 'email issues'."

"Order a 'Developer Laptop' for user 'Abraham Lincoln'."

👨‍💻 Contributing
Feel free to open an issue or submit a Pull Request!


### **Step 2: How to update it**

You have two ways to apply this:

**Option A: In VS Code (Recommended)**
1.  Open `README.md` in VS Code.
2.  Delete everything currently in there.
3.  Paste the code block above.
4.  Save (`Cmd+S`).
5.  Push to GitHub:
    ```bash
    git add README.md
    git commit -m "Update README formatting"
    git push
    ```

**Option B: Directly on GitHub.com**
1.  Go to your repository page.
2.  Click the **Pencil Icon** (✏️) on the `README.md` file.
3.  Paste the code block above.
4.  Click **"Commit changes..."** (green button).



### **Why this looks better**
* **`#`**: Makes big **Headings**.
* **` ```bash `**: Makes those nice grey **Code Boxes** so people can copy commands easily.
* **`**text**`**: Makes text **Bold**.
* **`---`**: Adds a horizontal divider line.
