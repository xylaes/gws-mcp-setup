---
name: google-workspace-cli
description: Interface with Google Workspace APIs (Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, etc.) using the Google Workspace CLI (gws).
---

# Google Workspace CLI Skill

Use this skill to guide your command formulation, scripting, and automation when interacting with Google Workspace services (Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, etc.) via the Google Workspace CLI (`gws`).

## Delegation Criteria
Use the Workspace CLI when you need to:
1. **Manage Files in Drive**: List files, search folders, download files, or upload reports.
2. **Read/Write Spreadsheets**: Get cell values from Google Sheets, update rows, or append logs.
3. **Automate Emails**: Send emails via Gmail, search for threads, or list message drafts.
4. **Coordinate Calendars**: Create events, list calendars, or check availability.
5. **Manage Documents/Docs**: Read/write documents or presentations.

---

## Windows Compatibility (Encoding Fix)

Always prefix `gws` commands with `$env:PYTHONIOENCODING="utf-8";` in Windows PowerShell to prevent `UnicodeEncodeError` when dealing with Unicode outputs:
```powershell
$env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli <command>
```

---

## Authentication status

Verify authentication status before running service commands:
```powershell
$env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli auth status
```

### Handing Unauthenticated State
If `auth_method` is `"none"` or authentication fails:
1. **STOP** and ask the user to run authentication.
2. Tell the user to run the following in their terminal:
   ```powershell
   # 1. Select / configure Google Cloud project context
   npx @googleworkspace/cli auth setup
   
   # 2. Login via Google OAuth2 browser flow
   npx @googleworkspace/cli auth login
   ```
3. Do **NOT** run these login commands yourself, as they require interactive browser confirmation.

---

## Command Syntax & Examples

Commands follow the structure:
`npx @googleworkspace/cli <service> <resource> [sub-resource] <method> [flags]`

Always output in JSON format (default) for easy parsing:

### 1. Google Drive
*   **List top 10 files**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli drive files list --params "{\`"pageSize\`": 10}"
    ```
*   **Search for Spreadsheets**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli drive files list --params "{\`"q\`": \`"mimeType = 'application/vnd.google-apps.spreadsheet'\`"}"
    ```

### 2. Google Sheets
*   **Read spreadsheet values**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli sheets spreadsheets values get --params "{\`"spreadsheetId\`": \`"YOUR_SPREADSHEET_ID\`", \`"range\`": \`"Sheet1!A1:D10\`"}"
    ```
*   **Append cell values**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli sheets spreadsheets values append --params "{\`"spreadsheetId\`": \`"YOUR_SPREADSHEET_ID\`", \`"range\`": \`"Sheet1!A1\`", \`"valueInputOption\`": \`"USER_ENTERED\`"}" --json "{\`"values\`": [[\`"Row Data 1\`", \`"Row Data 2\`"]]}"
    ```

### 3. Gmail
*   **List recent messages**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli gmail users messages list --params "{\`"userId\`": \`"me\`", \`"maxResults\`": 5}"
    ```
*   **Get message details**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli gmail users messages get --params "{\`"userId\`": \`"me\`", \`"id\`": \`"MESSAGE_ID\`"}"
    ```

### 4. Schema Helper
To inspect the API parameters and structure for any dynamic method:
```powershell
$env:PYTHONIOENCODING="utf-8"; npx @googleworkspace/cli schema drive.files.list
```
