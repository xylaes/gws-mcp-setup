# 🚀 Google Antigravity & Workspace MCP Labs

This repository documents the hands-on labs, custom implementations, and setup logs for Google Antigravity, custom agentic skills, Google Agent Development Kit (ADK), and custom Model Context Protocol (MCP) integrations.

---

## 🎯 Purpose of the Labs & Key Learning Objectives

This repository is designed as a structured learning journey to master building, configuring, and debugging modern agentic systems. Through these hands-on labs, developers learn:

* **Understanding Antigravity Agent Custom Skills:**
  * How to write and configure custom skills in the `.agents/skills` folder.
  * Moving from basic regex/keyword routing to multi-step procedural logic, few-shot prompting, and script-based schema validation.
  * Writing effective `SKILL.md` instruction files so that AI agents automatically discover and execute skills.
* **Building & Integrating Custom MCP Servers:**
  * Understanding the Model Context Protocol (MCP) and how it enables LLMs to interact with secure local or external resources.
  * Implementing custom Python `FastMCP` servers to securely fetch data (e.g., from the Google Calendar API) when official endpoints are restricted.
  * Troubleshooting named pipe conflicts, lock files, and local server integration.
* **GCP Authentication, OAuth, and API Scopes:**
  * Navigating Google Cloud IAM, scopes, and Application Default Credentials (ADC).
  * Bypassing security restrictions (such as CLI blocks on sensitive scopes like Google Calendar/Gmail) by creating custom Desktop App OAuth client IDs.
* **Developing State-based Graph Workflows (ADK 2.0):**
  * Building complex, stateful workflows with multiple nodes, conditional edges, and subagents.
  * Implementing advanced control flow, including dynamic routing using classification agents.
  * Handling execution state persistence and avoiding runtime crashes by setting `rerun_on_resume=True` on dynamic caller nodes.
  * Structuring custom function nodes to properly emit conversational `Event` objects for the CLI and Web UI.
* **Solving Environment-Specific Quirks:**
  * Troubleshooting Windows-specific and OneDrive-specific pathing, package locking, and shell wildcard expansion bugs.

---

## 📂 Project Structure

```
my-first-project/
├── .agents/                    # Custom Antigravity Skills (Levels 1 - 4)
│   ├── database-schema-validator/
│   ├── git-commit-formatter/
│   ├── json-to-pydantic/
│   └── license-header-adder/
├── antigravity-skills/         # Cloned official Antigravity reference skills
├── antigravity_skills_log.md   # Step-by-step verification log for skills & ADK
├── gws_mcp_setup_log.md        # Authentication, OAuth, and Local Calendar MCP log
├── local_calendar_mcp.py       # Custom Python FastMCP server for Google Calendar API v3
├── weather-assistant/          # Prototype agent created using agents-cli
└── ...
```

---

## 🛠️ Highlights & Solved Labs

### 1. Antigravity Skills (Levels 1 - 4)
We built and verified four progressive levels of agent capabilities:
* **Level 1: Basic Routing (`git-commit-formatter`)** - Conventional Commit formatter.
* **Level 2: Asset Utilization (`license-header-adder`)** - Prepends Apache 2.0 license headers dynamically.
* **Level 3: Few-Shot Learning (`json-to-pydantic`)** - Translates JSON objects into strongly-typed Pydantic classes.
* **Level 4: Procedural Logic & Validation (`database-schema-validator`)** - A custom python linter script checking SQL schemas for `DROP` commands, primary keys, and naming conventions.

### 2. Custom Local Calendar MCP Server
Due to Workspace Developer Preview restrictions on `@gmail.com` accounts, we bypassed remote endpoint blocks by implementing a **local MCP server** (`local_calendar_mcp.py`) using `FastMCP`:
* Authenticates directly using local Application Default Credentials (ADC).
* Bypasses client ID restrictions via custom desktop credentials.
* Exposes `list_calendars` and `list_events` directly to the LLM agent registry.

### 3. ADK 2.0 Graph Workflow Agent Lifecycle
Designed, run, and verified a routed graph workflow (`customer-support-agent`):
* Utilizes a classification node (`classify_query`) dynamically routing queries using `ctx.run_node` (configured with `rerun_on_resume=True` for resume robustness).
* Routes shipping-related queries to an LLM agent with playful emoji instructions and a $50 free shipping threshold trigger.
* Routes unrelated queries to a polite decline function node wrapping outputs in conversational `Event(message=...)` envelopes.

---

## ⚙️ How to Configure & Run

### Custom Calendar MCP Setup
1. Authenticate with custom desktop client ID scopes:
   ```powershell
   gcloud auth application-default login --client-id-file="C:\path\to\client_secret.json" --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/calendar.events"
   ```
2. Configure `mcp_config.json` inside your local AppData directory:
   ```json
   "local-calendar": {
     "command": "C:\\Users\\danny\\OneDrive\\Desktop\\my-first-project\\.venv\\Scripts\\python.exe",
     "args": [
       "C:\\Users\\danny\\OneDrive\\Desktop\\my-first-project\\local_calendar_mcp.py"
     ]
   }
   ```

### Running the ADK Dev Server
Avoid standard MSVC wildcard expansion crashes on Windows by running the ADK development playground server with escaped parameters:
```powershell
uv run adk web . --host 127.0.0.1 --port 8080 --allow_origins '`*' --reload_agents
```

---

## 📝 Detailed Lab Logs
* Detailed skills and ADK logs: [antigravity_skills_log.md](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/antigravity_skills_log.md)
* Detailed Google Workspace & local pipe MCP logs: [gws_mcp_setup_log.md](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/gws_mcp_setup_log.md)
