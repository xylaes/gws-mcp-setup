---
name: colab-cli
description: Use Google Colab CLI to provision remote compute runtimes (CPU, GPU, TPU) and execute code/scripts asynchronously.
---

# Google Colab CLI Skill

Use this skill when you need to provision cloud-based hardware (CPU, GPU, TPU) to execute Python scripts, train machine learning models, or run heavy data processing workloads on Google Colab.

## Delegation Criteria
Consider executing a script/notebook on Colab if:
1. **Accelerated Computing**: You need GPU (T4, L4, A100, H100) or TPU (v5e1, v6e1) acceleration.
2. **Resource Intensity**: The workload is too heavy or slow to run on the local user machine.
3. **Environment Isolation**: You need a clean, cloud-hosted Linux environment with pre-installed data science packages.

---

## Windows Compatibility (Encoding Fix)

When running `colab` commands on Windows PowerShell, prepend `$env:PYTHONIOENCODING="utf-8";` to prevent `UnicodeEncodeError` when the CLI outputs Unicode formatting:
```powershell
$env:PYTHONIOENCODING="utf-8"; colab <command>
```

---

## Authentication and Pre-flight

1. Verify authentication status:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; colab sessions
   ```
2. If authorization fails (HTTP 401 or 403), verify scopes and account:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; colab whoami
   ```
3. To configure ADC with correct scopes:
   ```powershell
   gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/colaboratory
   ```

---

## Usage Workflow

### 1. Provision a Runtime
Always specify a session name (`-s <name>`) to avoid ambiguous generated session IDs.
*   **CPU Runtime**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab new -s my-session
    ```
*   **GPU Runtime** (e.g. T4, L4, A100):
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab new -s my-session --gpu T4
    ```
*   **TPU Runtime** (e.g. v6e1):
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab new -s my-session --tpu v6e1
    ```

### 2. Execute Code
*   **Run a Python script**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab exec -s my-session -f script.py
    ```
*   **Run a Jupyter notebook**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab exec -s my-session -f notebook.ipynb
    ```
    *This runs each cell and outputs `<basename>_output.ipynb` locally.*
*   **Install package dependencies**:
    ```powershell
    $env:PYTHONIOENCODING="utf-8"; colab install -s my-session -r requirements.txt
    ```

### 3. Ephemeral Run (One-Shot execution)
To provision a fresh runtime, execute a script, and automatically stop/tear down the VM:
```powershell
$env:PYTHONIOENCODING="utf-8"; colab run script.py
```
*Add `--gpu <type>` or `--tpu <type>` to run with accelerators.*

### 4. Clean up (CRITICAL)
Idle runtimes continue to consume compute units. Always release the VM when finished:
```powershell
$env:PYTHONIOENCODING="utf-8"; colab stop -s my-session
```
