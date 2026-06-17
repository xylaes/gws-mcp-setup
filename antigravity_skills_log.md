# Google Antigravity & agents-cli Codelab Setup Log

This document serves as a permanent record of the walkthrough, execution, and verification steps performed during the **Google Antigravity Skills and CLI Codelab** tutorial.

---

## 📋 Codelab Overview
* **Target Environment:** Windows 10, personal Google Account (`dannyjriggleman09@gmail.com`), Google Cloud project `gen-lang-client-0720914706`.
* **Workspace:** `c:\Users\danny\OneDrive\Desktop\my-first-project`
* **Repository:** [gws-mcp-setup](https://github.com/xylaes/gws-mcp-setup)

---

## 🛠️ Part 1: Antigravity Skills Tutorial (Levels 1 - 4)

We cloned the official [antigravity-skills repository](https://github.com/rominirani/antigravity-skills) and progressive levels of complexity:

### Level 1: Basic Routing (`git-commit-formatter`)
* **Objective:** Intercept "commit" requests and format git commit messages according to the Conventional Commits specification.
* **Actions:**
  1. Copied `git-commit-formatter` to `.agents/skills/git-commit-formatter`.
  2. Created a test git repository inside `git_test/`.
  3. Added Google login functionality to `auth.py`.
  4. Staged the changes and committed them using the Conventional Commits formatting:
     ```bash
     git commit -m "feat(auth): implement login with google"
     ```
  5. Verified the message formatting using `git log`.

### Level 2: Asset Utilization (`license-header-adder`)
* **Objective:** Automatically prepend a static Apache 2.0 license template, adjusted for target language comments, to newly created source files.
* **Actions:**
  1. Copied `license-header-adder` to `.agents/skills/license-header-adder`.
  2. Read the template from `resources/HEADER_TEMPLATE.txt`.
  3. Created `my_script.py` and prepended the license template converted to Python `#` comments.

### Level 3: Few-Shot Learning (`json-to-pydantic`)
* **Objective:** Leverage "golden example" input-output pairs to convert JSON structures into Pydantic models.
* **Actions:**
  1. Copied `json-to-pydantic` to `.agents/skills/json-to-pydantic`.
  2. Created `product.json` containing:
     ```json
     {
       "product": "Widget",
       "cost": 10.99,
       "stock": null
     }
     ```
  3. Generated a strongly-typed Pydantic schema in `product_model.py` based on the few-shot examples:
     ```python
     from pydantic import BaseModel
     from typing import Optional

     class Product(BaseModel):
         product: str
         cost: float
         stock: Optional[int] = None
     ```

### Level 4: Procedural Logic & Validation (`database-schema-validator`)
* **Objective:** Execute deterministic validation scripts to check SQL schemas for naming styling, safety (no `DROP` statements), and primary keys.
* **Actions:**
  1. Copied `database-schema-validator` to `.agents/skills/database-schema-validator`.
  2. Created a test `bad_schema.sql` file containing unsafe `DROP TABLE` statements, non-snake_case names, and missing primary keys.
  3. Ran the validator script:
     ```powershell
     python .agents/skills/database-schema-validator/scripts/validate_schema.py bad_schema.sql
     ```
  4. Captured the expected error output:
     * `ERROR: 'DROP TABLE' statements are forbidden.`
     * `ERROR: Table 'userProfile' must be snake_case.`
     * `ERROR: Table 'posts' is missing a primary key named 'id'.`

---

## 🚀 Part 2: `agents-cli` and ADK Web Server Setup

We configured the Google Agent Development Kit (ADK) and ran the `weather-assistant` prototype:

### 1. Installation & Init
* Installed `uv` package manager.
* Ran setup to configure Application Default Credentials and fetch global skills:
  ```powershell
  uvx google-agents-cli setup
  ```
* Created the prototype weather agent structure:
  ```powershell
  uvx google-agents-cli create weather-assistant --prototype --yes
  ```
* Installed Python environment dependencies:
  ```powershell
  uvx google-agents-cli install
  ```

### 2. Local CLI Testing
* Initiated the agent locally and queried it:
  ```powershell
  uvx google-agents-cli run "How are you?"
  ```
* **Response Received:**
  > `[root_agent]: I am an AI assistant, and I don't have feelings, but I'm ready to help you with any questions or tasks you have! How can I assist you today?`

### 3. Agent Playground UI
* Encountered a Windows-specific wildcard expansion bug with `agents-cli playground` caused by MSVC expanding the `--allow_origins "*"` argument.
* Resolved by launching the ADK web server manually with escaped parameters:
  ```powershell
  uv run adk web . --host 127.0.0.1 --port 8080 --allow_origins '`*' --reload_agents
  ```
* The **Agent Playground UI** successfully started and is accessible locally at:
  [http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)

---

## 🚀 Part 3: `agents-cli-adk-lifecycle` CodeLab (Graph Workflows)

We created a graph-based workflow agent called `customer-support-agent` using **ADK 2.0**:

### 1. Creation and File System Workaround
* Initialized the project without deployment files:
  ```powershell
  uvx google-agents-cli create customer-support-agent --agent adk --prototype --yes
  ```
* Encountered a Windows/OneDrive filesystem hardlink error (`os error 396`) during dependency installation.
* Resolved by setting `UV_LINK_MODE="copy"` to force copies instead of hardlinks:
  ```powershell
  $env:UV_LINK_MODE="copy"; uvx google-agents-cli install
  ```

### 2. Graph Workflow Design
We updated `app/agent.py` to route users based on query classification:
* **START**: Enters the user query.
* **`classify_query`** (Function Node): Uses a nested `classifier_agent` to determine if the query is `"shipping"` or `"unrelated"`.
* **`shipping_faq_agent`** (LLM Node): An agent styled with playful emojis that answers shipping questions and highlights the **$50 free shipping threshold**.
* **`politely_decline`** (Function Node): A Python node returning a static message politely refusing to answer non-shipping queries.
* **Edges**: 
  * `(START, classify_query)`
  * `(classify_query, {"shipping": shipping_faq_agent, "unrelated": politely_decline})`

### 3. Key Troubleshooting & Technical Fixes
1. **Dynamic Node scheduling requirements:**
   * **Problem:** Running `ctx.run_node` inside `classify_query` crashed because the caller node lacked resume permissions.
   * **Resolution:** Set `rerun_on_resume=True` on the `@node` decorator:
     ```python
     @node(rerun_on_resume=True)
     async def classify_query(ctx: Context, node_input: str) -> Event:
     ```
2. **Coerced Type Correction:**
   * **Problem:** Invoking `ctx.run_node(...)` on an agent returned a raw string, causing `response.text` to throw `AttributeError: 'str' object has no attribute 'text'`.
   * **Resolution:** Accessed the response directly as a string (`response.strip().lower()`).
3. **Conversational Function Node Output:**
   * **Problem:** Returning a raw string from `politely_decline` yielded an output event, but didn't display a text bubble in the CLI/Playground.
   * **Resolution:** Modified the function return value to wrap it in a proper `Event` containing a message:
     ```python
     return Event(message="I'm sorry, but I can only assist with...")
     ```

### 4. Successful Verification Logs
* **Shipping Query:**
  ```
  [user]: How much is standard shipping?
  [classifier_agent]: shipping
  [shipping_faq_agent]: OH MY GOSH! 🤩 ... If your order total is $50 or more, standard shipping is 100% FREE! 🎉💰
  ```
* **Duration Query:**
  ```
  [user]: How long does standard delivery take?
  [classifier_agent]: shipping
  [shipping_faq_agent]: you can expect your awesome items to arrive usually within 5 to 7 business days! 🗓️
  ```
* **Unrelated Query:**
  ```
  [user]: What is the capital of France?
  [classifier_agent]: unrelated
  [politely_decline]: I'm sorry, but I can only assist with questions related to shipping...
  ```

