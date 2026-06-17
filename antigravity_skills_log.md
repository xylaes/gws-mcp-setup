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
