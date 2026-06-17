# Google Workspace & Local Calendar MCP Setup Log

This document serves as a permanent record of the troubleshooting steps, discoveries, and solutions implemented to get Google Calendar and local named pipe MCP servers working in the Antigravity IDE.

---

## 📋 Overview of the Objectives
1. **Google Workspace MCP:** Connect Google Calendar tools to the Antigravity IDE.
2. **Local MCP Servers:** Fix the `connect ENOENT` pipe errors on `notebooks` and `visualization` servers.
3. **Target Environment:** Windows 10, personal Google Account (`dannyjriggleman09@gmail.com`), Google Cloud project `gen-lang-client-0720914706`.

---

## 🛠️ Summary of Actions & Resolutions

### 1. Local Named Pipes (`notebooks` & `visualization`)
* **Symptom:** AI returned `connect ENOENT \\?\pipe\datacloud-mcp-notebooks-antigravityide`.
* **Root Cause:** Multiple orphaned background processes of `mcp_proxy_bundle.js` from previous sessions were holding pipe handles or in a bad state.
* **Resolution:** Cleared all orphaned Node processes:
  ```powershell
  Get-CimInstance Win32_Process -Filter "name = 'node.exe'" | Where-Object { $_.CommandLine -like "*mcp_proxy_bundle.js*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
  ```
  After restarting, the named pipes were successfully initialized by the IDE extension at `\\.\pipe\datacloud-mcp-notebooks-antigravityide` and connected.

---

### 2. Official Google Workspace MCP Permission Blocks
* **Symptom:** `gws-calendar` server calls (e.g. `list_events`) returned `The caller does not have permission` (403 Forbidden).
* **Investigation:**
  * Checked enabled APIs in project: both `calendar-json.googleapis.com` and `calendarmcp.googleapis.com` were active.
  * Added the missing **MCP Tool User** role (`roles/mcp.toolUser`) to the user account:
    ```bash
    gcloud projects add-iam-policy-binding gen-lang-client-0720914706 --member="user:dannyjriggleman09@gmail.com" --role="roles/mcp.toolUser"
    ```
* **Discovery:** The official remote endpoint `https://calendarmcp.googleapis.com/mcp/v1` is restricted under the **Google Workspace Developer Preview Program**. Standard personal `@gmail.com` accounts are blocked at the gateway level unless whitelisted in the preview.

---

### 3. CLI OAuth Scope Block ("This App is Blocked")
* **Symptom:** Running `gcloud auth application-default login --scopes=...` with calendar scopes resulted in a red Google block screen ("This app is blocked").
* **Root Cause:** Google blocks the default `gcloud` CLI OAuth client ID from requesting sensitive scopes (like Calendar/Gmail) to prevent phishing.
* **Resolution:** 
  1. Created a custom **Desktop app** OAuth Client ID in Google Cloud Console (**APIs & Services > Credentials**).
  2. Downloaded the secrets JSON file.
  3. Re-authenticated using the custom client ID and explicit scopes:
     ```powershell
     gcloud auth application-default login --client-id-file="C:\path\to\client_secret.json" --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.readonly,https://www.googleapis.com/auth/calendar.events"
     ```
  4. Decoded the token using Google's tokeninfo endpoint, verifying that the new token successfully possesses all requested Calendar scopes.

---

### 4. Custom Local Calendar MCP (Alternative Working Solution)
Since the official remote MCP endpoint is gated, we created a **local MCP server** that queries the standard Google Calendar API v3 directly (which is fully functional and authorized under your local credentials).

* **Server Script (`local_calendar_mcp.py`):**
  * Created inside the workspace using Python `FastMCP`.
  * Automatically retrieves local Application Default Credentials (ADC) token:
    ```python
    credentials, project = google.auth.default()
    ```
  * Exposes `list_calendars` and `list_events` tools directly to the AI.
* **IDE Integration (`mcp_config.json`):**
  Registered the server in `C:\Users\danny\.gemini\antigravity\mcp_config.json`:
  ```json
  "local-calendar": {
    "command": "c:\\Users\\danny\\OneDrive\\Desktop\\my-first-project\\.venv\\Scripts\\python.exe",
    "args": [
      "c:\\Users\\danny\\OneDrive\\Desktop\\my-first-project\\local_calendar_mcp.py"
    ]
  }
  ```

---

## 📌 Re-activation Checklist (For future reference)
If the calendar tools stop working, follow these quick check steps:
1. **Refresh Token:** Run `gcloud auth application-default print-access-token` in terminal. If expired, run the custom client-id login command (Step 3 above).
2. **Sync Config:** In the IDE, run `Google Cloud Data Agent Kit: Sync Config from Google Cloud CLI to Extension`.
3. **Reload Window:** Reload the IDE window (`Developer: Reload Window`) to refresh the local tool registries.
