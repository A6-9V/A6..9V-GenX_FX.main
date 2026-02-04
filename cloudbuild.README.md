# Google Cloud Build Configuration (Optional)

⚠️ **Note:** These Cloud Build configurations are OPTIONAL and should only be used if you're deploying to Google Cloud Run.

## Files

- `cloudbuild.yaml` - Builds and deploys Exness EA to Cloud Run (europe-west1)
- `cloudbuild.immediate.yaml` - Builds and deploys main trading system to Cloud Run (us-central1)

## Usage

### Prerequisites
1. Google Cloud Project with Cloud Build and Cloud Run APIs enabled
2. Configured authentication via `gcloud`
3. Docker registry access

### Manual Trigger
```bash
# For Exness EA deployment
gcloud builds submit --config=cloudbuild.yaml

# For main trading system
gcloud builds submit --config=cloudbuild.immediate.yaml
```

### Automatic Trigger
You can set up Cloud Build triggers in your Google Cloud Console to automatically build on:
- Push to specific branches
- Push to specific tags
- Manual trigger via console

## Default Platform

**GitHub Actions** is the primary CI/CD platform for this project. See [DEPLOYMENT_STRATEGY.md](DEPLOYMENT_STRATEGY.md) for more information.

Only use Cloud Build if you specifically need to deploy to Google Cloud Run. Otherwise, disable or ignore these files to avoid confusion and redundant deployments.

## Disabling Cloud Build

If you're not using Google Cloud Run, you can safely ignore these files. They will not automatically trigger unless you have Cloud Build triggers configured in your Google Cloud Project.

To completely disable:
1. Don't configure Cloud Build triggers in Google Cloud Console
2. Optionally rename files to `.disabled`: 
   ```bash
   mv cloudbuild.yaml cloudbuild.yaml.disabled
   mv cloudbuild.immediate.yaml cloudbuild.immediate.yaml.disabled
   ```
