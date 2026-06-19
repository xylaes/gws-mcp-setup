# 🛠️ Google Workspace & Local Calendar MCP Lab

This repository serves as a hands-on lab and reference log for connecting **Google Workspace** services and custom local tools to the **Google Antigravity IDE/CLI** using the **Model Context Protocol (MCP)**.

---

## 🎯 Lab Purpose

The goal of this lab is to demonstrate how to bridge the gap between LLM agents and personal productivity hubs. It explores the configuration of secure remote MCP gateways, the debugging of local IPC (named pipes) channels, and the development of custom Python-based local MCP server alternatives using standard APIs.

---

## 🧠 Key Learning Objectives

By working through this lab, you will learn several high-value integration concepts:

### 1. The Model Context Protocol (MCP) Architecture
* How LLMs dynamically discover, request, and execute client-side tools.
* The difference between official remote MCP endpoints (like Google's Workspace gateways) and local MCP servers.

### 2. Google Cloud Platform (GCP) & OAuth Security
* Setting up custom **OAuth Consent Screens** and configuring precise data access scopes (Gmail, Calendar, Drive, Chat, and People).
* Bypassing security restrictions (such as Google's "This App is Blocked" screen) by creating specialized **Desktop App credentials** rather than default CLI profiles.
* Managing and verifying local **Application Default Credentials (ADC)** tokens.

### 3. Creating Custom MCP Servers
* Writing lightweight, fast-loading MCP servers in Python using the `FastMCP` framework.
* Mapping standard REST APIs (e.g., Google Calendar API v3) to MCP tools with zero hardcoded credentials, leveraging system-level tokens.

### 4. IPC & IDE Infrastructure Debugging
* Diagnosing named pipe locks (`connect ENOENT`) on Windows environments caused by orphaned background proxy processes.
* Managing IDE config files (`mcp_config.json`) to register and sync local executable paths.

---

## 📂 Repository Structure

* 📄 **[README.md](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/README.md)**: Main landing page summarizing the lab goals and learnings.
* 📝 **[gws_mcp_setup_log.md](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/gws_mcp_setup_log.md)**: A detailed chronological log of the configuration commands, issues encountered (such as Developer Preview API gates), and their technical resolutions.
* 🐍 **[local_calendar_mcp.py](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/local_calendar_mcp.py)**: The custom FastMCP server script running a direct Google Calendar integration.
* ⚙️ **[.gitignore](file:///c:/Users/danny/OneDrive/Desktop/my-first-project/.gitignore)**: Standard ignores to prevent committing environment packages (`.venv`) and system assets.
