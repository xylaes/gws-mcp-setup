# Get the active project ID from gcloud config
$projectId = (gcloud config get-value project)
if (-not $projectId) {
    Write-Error "No active gcloud project found. Please run 'gcloud config set project YOUR_PROJECT_ID' first."
    exit
}

Write-Host "Using GCP Project: $projectId"

# 1. Create the Pub/Sub topic if it doesn't already exist
Write-Host "Creating Pub/Sub topic 'billing-alerts'..."
gcloud pubsub topics create billing-alerts 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Successfully created topic 'billing-alerts'."
} else {
    Write-Host "Topic 'billing-alerts' already exists or creation skipped."
}

# 2. Deploy the Cloud Function
Write-Host "Deploying Cloud Function 'cap-billing'..."
gcloud functions deploy cap-billing `
    --runtime=python310 `
    --trigger-topic=billing-alerts `
    --entry-point=cap_billing `
    --region=us-central1 `
    --source="$PSScriptRoot" `
    --allow-unauthenticated

if ($LASTEXITCODE -ne 0) {
    Write-Error "Cloud Function deployment failed."
    exit
}

# 3. Bind the Project Billing Manager role to the default service account
Write-Host "Granting Project Billing Manager role to default App Engine Service Account..."
$serviceAccount = "$projectId@appspot.gserviceaccount.com"

gcloud projects add-iam-policy-binding $projectId `
    --member="serviceAccount:$serviceAccount" `
    --role="roles/billing.projectManager"

Write-Host "Setup complete!"
Write-Host "Ensure you now link your $100 budget in the billing console to the 'billing-alerts' Pub/Sub topic."
