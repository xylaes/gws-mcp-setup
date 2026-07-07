# Next Steps: Google Chat Integration (Option 1)

## Goal
Establish a secure, real-time connection between a Google Chat space and the local Antigravity agent running on your desktop. This will allow you to query and assign tasks to Antigravity directly from Google Chat on any device.

## Selected Architecture: Option 1 (Pub/Sub Pull)
This architecture is selected because it works through firewalls/NAT without requiring public tunnels (like ngrok) or exposing local ports.

```
+-------------+      Events      +-------------------+      Pull      +------------------+
| Google Chat | -------------->  | Cloud Pub/Sub     | <------------- | Local Subscriber |
| (App/Bot)   |                  | (Topic/Sub)       |                | (Desktop Script) |
+-------------+                  +-------------------+                +------------------+
                                                                               |
                                                                               | Executes
                                                                               v
+-------------+      Replies     +-------------------+                +------------------+
| Google Chat | <--------------  | Workspace CLI     | <------------- | Local Agent      |
| Space       |                  | (gws chat/API)    |                | (Antigravity)    |
+-------------+                  +-------------------+                +------------------+
```

---

## Action Plan for Next Session

### Step 1: Google Cloud Console Setup
1. Open the GCP Console for project `gen-lang-client-0720914706`.
2. Go to **Pub/Sub > Topics** and create a new topic named `google-chat-events`.
3. Create a **Pull subscription** for that topic named `desktop-agent-listener`.
4. Grant the Google Chat Service Account permission to publish to your topic (Chat Developer Console will guide this).

### Step 2: Google Chat App Registration
1. In GCP Console, search for **Google Chat API** and enable it if needed.
2. In the **Configuration** tab of the Chat API, set up your bot:
   * **App Name**: Antigravity Local
   * **Connection settings**: Select **Cloud Pub/Sub** and enter your topic path (`projects/gen-lang-client-0720914706/topics/google-chat-events`).

### Step 3: Implement Local Pub/Sub Listener
Create a Python script (e.g. `google_chat_listener.py`) running locally that:
1. Pulls events from the `desktop-agent-listener` subscription using `google-cloud-pubsub`.
2. Extracts the user's message.
3. Invokes the local agent recursively:
   ```powershell
   agents-cli run "User message from Chat"
   ```
4. Parses the response and posts it back to Google Chat using the dynamic Workspace CLI:
   ```powershell
   npx @googleworkspace/cli chat spaces messages create --params "{\"parent\": \"spaces/SPACE_ID\"}" --json "{\"text\": \"Agent response...\"}"
   ```

### Step 4: Daemonize/Background Service
Configure the listener script to run continuously on Windows start (e.g., via a silent PowerShell script or Windows Task Scheduler).
