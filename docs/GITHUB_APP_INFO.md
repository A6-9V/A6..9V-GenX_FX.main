# GitHub App Configuration

**App Name:** GenX
**Client ID:** Ov23liVH34OCl6XkcrH6
**Client Secret:** 0d3e2e9052a4d553c39a2780ebde2c5f1e60d4c6
**Homepage URL:** https://studio.firebase.google.com/historymaker-1-06020501
**Authorization callback URL:** https://github.com/Mouy-leng/A6-9V/admin/auth/handler

## Setup Instructions

1. Copy the Client ID and Client Secret to your `.env` file:
   ```bash
   GITHUB_CLIENT_ID=Ov23liVH34OCl6XkcrH6
   GITHUB_CLIENT_SECRET=0d3e2e9052a4d553c39a2780ebde2c5f1e60d4c6
   GITHUB_CALLBACK_URL=https://github.com/Mouy-leng/A6-9V/admin/auth/handler
   ```

2. If using `setup_github_secrets.sh`, enter these values when prompted.

**Note:** The callback URL provided (`https://github.com/Mouy-leng/A6-9V/admin/auth/handler`) points to a file in the GitHub repository. Ensure this is the intended behavior. Typically, callback URLs point to your application's running instance (e.g., `https://your-app.com/auth/callback`).
