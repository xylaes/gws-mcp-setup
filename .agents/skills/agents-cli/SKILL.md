---
name: agents-cli
description: Use the Agents CLI tool to build, run (recursively), evaluate, and deploy agent projects.
---

# Google Agents CLI Skill

Use this skill when you want to build, scaffold, evaluate, deploy, or run agent projects locally or remotely. Specifically, you can use the `run` command to recursively delegate sub-tasks to other local or remote agents.

## Delegation and Lifecycle Criteria
Use the `agents-cli` tool if:
1. **Recursive Execution**: You want to spin up a subagent (either locally or remotely) to handle a specific sub-task and return the result.
2. **Local Playground**: You or the user want to run a local web-based playground interface for testing the agent project.
3. **Agent Evaluations**: You need to run evaluation generation or grading runs.
4. **Scaffolding and Deployment**: You are creating a new agent project or deploying an existing one to Google Cloud.

---

## Workspace Context

Commands like `agents-cli run`, `playground`, and `eval` must be executed from within an agent project directory (e.g., `ambient-expense-agent/` or `caretaker-ai/`), or you must specify the `--app-name` flag when calling from the project root.

---

## Usage Workflow

### 1. Recursive Sub-task Execution
To send a prompt to the project's agent and receive the response:
*   **One-off run**:
    ```powershell
    agents-cli run "Prompt for the agent to execute"
    ```
*   **Persistent Server run** (Recommended for speed and session preservation):
    ```powershell
    agents-cli run --start-server "Initial prompt for the agent"
    ```
*   **Conversation Continuity** (Resume a session on the persistent server):
    ```powershell
    agents-cli run --session-id "my-session-123" "Follow-up prompt"
    ```
*   **Query Deployed/Remote Agent**:
    ```powershell
    agents-cli run --url "https://my-agent-url" --mode adk "Prompt for the remote agent"
    ```

### 2. local Agent Playground
To start a local interactive web playground for testing:
```powershell
agents-cli playground
```

### 3. Evaluation Suites
To evaluate the agent project's performance on datasets:
1. Generate traces over evaluation test cases:
   ```powershell
   agents-cli eval generate
   ```
2. Grade the generated traces:
   ```powershell
   agents-cli eval grade
   ```

### 4. Project Creation and Scaffold
*   Create a new agent from templates:
    ```powershell
    agents-cli create <new-agent-name>
    ```
*   Add deployment, CI/CD, or enhance project structure:
    ```powershell
    agents-cli scaffold enhance .
    ```
