# 🚂 Railway Deployment Guide

This guide provides step-by-step instructions for deploying the GenX FX Trading Platform to [Railway](https://railway.com?referralCode=AHRe-w).

## 🚀 Why Railway?

Railway is a modern deployment platform that makes it easy to deploy full-stack applications with multiple services (Python + Node.js) and databases (Redis, PostgreSQL, etc.).

## 📋 Prerequisites

1.  A Railway account. Use this link to get started: [https://railway.com?referralCode=AHRe-w](https://railway.com?referralCode=AHRe-w)
2.  The Railway CLI installed locally (optional but recommended): `npm i -g @railway/cli`
3.  Your repository pushed to GitHub.

## 🛠️ Step-by-Step Deployment

### 1. Create a New Project

1.  Log in to [Railway](https://railway.com?referralCode=AHRe-w).
2.  Click on **"New Project"**.
3.  Select **"Deploy from GitHub repo"**.
4.  Choose your `GenX_FX` repository.

### 2. Configure Build & Deploy Settings

Railway will automatically detect the `railway.json` file in the root of your repository. It uses the following configuration:

- **Builder**: NIXPACKS (automatically detects Python and Node.js)
- **Start Command**: `npm run start:prod` (starts both the Node.js server and Python FastAPI backend)

### 3. Add Environment Variables

In your Railway project, navigate to the **Variables** tab and add the necessary environment variables:

| Variable | Description |
| :--- | :--- |
| `NODE_ENV` | Set to `production` |
| `SECRET_KEY` | A long, random string for security |
| `REDIS_URL` | URL for your Redis instance (see Step 4) |
| `DATABASE_URL` | URL for your database (if using external DB) |
| `FXCM_ACCESS_TOKEN` | (Optional) Your FXCM API token |
| `BYBIT_API_KEY` | (Optional) Your Bybit API key |
| `BYBIT_API_SECRET` | (Optional) Your Bybit API secret |

### 4. Add Redis (Optional but Recommended)

For features like health check caching and system monitoring, you should add a Redis service to your project:

1.  Click **"Add Service"** in your Railway project.
2.  Select **"Database"** -> **"Redis"**.
3.  Railway will automatically provide a `REDIS_URL` environment variable to your main service.

## 🔍 Verification

Once the deployment is complete, you can verify it by:

1.  Visiting the public URL provided by Railway.
2.  Checking the `/health` endpoint (e.g., `https://your-app.up.railway.app/health`).
3.  Checking the `/api/v1/health` endpoint for the Python backend status.

## 🧪 Local Testing

Before deploying, you can test the production start command locally:

```bash
npm run start:prod
```

This will start both services concurrently on your local machine.

---

**Happy Trading!** 📈

*Support the project by using our referral link: [https://railway.com?referralCode=AHRe-w](https://railway.com?referralCode=AHRe-w)*
