# 🚂 Railway Deployment Guide

This guide provides step-by-step instructions for deploying the GenX FX Trading System on [Railway](https://railway.com?referralCode=AHRe-w).

## 🚀 Quick Deploy

The fastest way to deploy is using the referral link:

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/new/template?template=https%3A%2F%2Fgithub.com%2FMouy-leng%2FGenX_FX&referralCode=AHRe-w)

## 🛠️ Manual Deployment

If you prefer to deploy manually or from your own fork:

### 1. Create a Railway Project
1. Log in to your [Railway account](https://railway.com?referralCode=AHRe-w).
2. Click on **"New Project"**.
3. Select **"Deploy from GitHub repo"**.
4. Choose your repository.

### 2. Configure Build & Deploy Settings
Railway should automatically detect the configuration from `railway.json`, but ensure these settings are correct:

- **Build Command**: Nixpacks will handle this automatically (it will run `npm install`, `pip install`, and `npm run build`).
- **Start Command**: `npm start`
- **Port**: Railway will automatically assign a port and set the `PORT` environment variable.

### 3. Set Environment Variables
Add the following environment variables in the **Variables** tab:

| Variable | Description | Default/Example |
|----------|-------------|-----------------|
| `NODE_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Secret key for FastAPI | (Random string) |
| `JWT_SECRET` | Secret key for JWT | (Random string) |
| `REDIS_HOST` | Redis hostname | (From Redis addon) |
| `REDIS_PORT` | Redis port | (From Redis addon) |
| `DATABASE_URL` | PostgreSQL URL | (From Postgres addon) |

### 4. Add Services (Optional but Recommended)
For full functionality, you should add these services to your Railway project:
- **Redis**: For caching and real-time metrics.
- **PostgreSQL**: If you plan to move away from SQLite for production persistence.

## 📁 Repository Structure for Railway

- `railway.json`: Main configuration file for Railway.
- `Procfile`: Fallback configuration for Heroku-like environments.
- `package.json`: Contains the `start` script that runs both Node.js and Python servers.
- `api/main.py`: The FastAPI backend (listens on port 8000 internally).
- `services/server/index.ts`: The Node.js WebSocket server and proxy (listens on `$PORT`).

## 🔍 Verification
Once deployed, you can verify the deployment by visiting:
- `https://your-app-name.railway.app/` - The main dashboard.
- `https://your-app-name.railway.app/health` - Health check endpoint.
- `https://your-app-name.railway.app/api/v1/health` - API health check.

## 🆘 Troubleshooting

### Port Issues
If the app fails to bind to the port, ensure that the Node.js server is using `process.env.PORT` and the Python server is using port `8000`.

### Database Persistence
Note that SQLite (`genxdb_fx.db`) is ephemeral on Railway unless you use a Volume. For production, it is highly recommended to use the PostgreSQL addon.

---
*Support the project by using the [referral link](https://railway.com?referralCode=AHRe-w) when signing up!*
