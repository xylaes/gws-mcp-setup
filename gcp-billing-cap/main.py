import base64
import json
import os
from google.cloud import billing_v1

# Initialize the client once outside the function to reuse across invocations
billing_client = billing_v1.CloudBillingClient()

# The project ID where you want to disable billing
PROJECT_ID = (
    os.environ.get("GCP_PROJECT")
    or os.environ.get("GOOGLE_CLOUD_PROJECT")
)
    or "gen-lang-client-0720914706"
)


def cap_billing(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload containing the Pub/Sub message envelope.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # 1. Decode the Pub/Sub message
    if "data" not in event:
        print("No data in Pub/Sub event.")
        return

    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    data = json.loads(pubsub_message)

    cost_amount = data.get("costAmount", 0.0)
    budget_amount = data.get("budgetAmount", 0.0)

    print(f"Current cost: ${cost_amount:.2f}, Budget limit: ${budget_amount:.2f}")

    # 2. Check if we have met or exceeded the budget limit ($100)
    if cost_amount >= budget_amount:
        if not PROJECT_ID:
            print("Error: Project ID could not be determined. Please set GCP_PROJECT or GOOGLE_CLOUD_PROJECT.")
            return

        print(
            f"Cost of ${cost_amount:.2f} meets or exceeds budget limit of ${budget_amount:.2f}. Disabling billing..."
        )
        disable_billing(PROJECT_ID)
    else:
        print(f"Current cost of ${cost_amount:.2f} is within budget. No action taken.")


def disable_billing(project_id):
    """Disable billing for the specified project by removing its billing account."""
    project_name = f"projects/{project_id}"

    # Setting billing_account_name to an empty string disables billing on the project
    billing_info = billing_v1.ProjectBillingInfo(billing_account_name="")

    try:
        response = billing_client.update_project_billing_info(
            name=project_name, project_billing_info=billing_info
        )
        print(f"Successfully disabled billing for {project_id}: {response}")
    except Exception as e:
        print(f"Failed to disable billing for {project_id}: {e}")
        raise e
