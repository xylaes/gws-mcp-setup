---
name: jules-agent
description: Delegate complex, tedious, or long-running coding tasks to Jules (Google's asynchronous autonomous coding agent) using the Jules CLI.
---

# Jules Agent Skill

Use this skill when you want to hand off large, tedious, or long-running tasks to Jules, Google's autonomous background coding agent.

## Delegation Criteria
Consider delegating a task to Jules if it is:
1. **Large or Tedious**: Writing unit tests for a newly created module/directory, adding boilerplate, or renaming/refactoring symbols across many files.
2. **Asynchronous/Long-running**: Tasks that take several minutes to run and would block the interactive conversation.
3. **Well-Defined**: The instructions can be expressed clearly in a single prompt (e.g., "Implement exhaustive unit tests for app/utils.py covering all edge cases").

Do NOT delegate if:
- The task requires local device hardware, local emulator access, or interactive UI debugging.
- The task is a quick, one-off edit that can be done instantly.

---

## Authentication Check

Before calling any Jules commands, verify that you are authenticated:
```powershell
jules remote list --repo
```

### Handling Authentication Errors
If the command fails with a `401` error (e.g., "Request is missing required authentication credential"):
1. **STOP** and inform the user.
2. Instruct the user to run `jules login` in their terminal to authenticate.
3. Do **NOT** run `jules login` yourself, as it opens an interactive browser-based OAuth flow which cannot complete in a headless agent terminal.

---

## Usage Workflow

### 1. Create a Task
Create a new task in the current repository:
```powershell
jules new "Detailed description of the task for Jules to execute"
```
Or for a specific repository:
```powershell
jules remote new --repo "owner/repo" --session "Detailed description of the task"
```
*Note the session ID returned by this command (e.g., `123456`).*

### 2. Monitor Progress
To check the status of your tasks and list active sessions:
```powershell
jules remote list --session
```

### 3. Pull and Apply Changes
Once Jules reports that the task is finished:
- Pull and apply the changes directly to your local workspace:
  ```powershell
  jules remote pull --session <session_id> --apply
  ```
- Or use `teleport` to apply changes:
  ```powershell
  jules teleport <session_id>
  ```

---

## Verification and Hand-back
After applying Jules' changes:
1. Run local tests or build steps to verify that the changes are correct and compile properly.
2. Review the diff of the changes.
3. Report back to the user with the result and a summary of what Jules accomplished.
