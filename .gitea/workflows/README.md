# Gitea Workflows (Optional)

⚠️ **Note:** This Gitea workflow configuration is OPTIONAL and should only be enabled if you're using Gitea for self-hosted deployments to a specific VPS.

## Configuration

The `deploy-vps.yml` workflow:
- Builds Docker images using `Dockerfile.production`
- Pushes to Docker Hub as `mouyleng/genx-fx`
- Deploys to VPS via SSH
- Performs health checks
- Sends Telegram notifications
- Creates database backups

## Default Platform

**GitHub Actions** is the primary CI/CD platform for this project. See [DEPLOYMENT_STRATEGY.md](../../DEPLOYMENT_STRATEGY.md) for more information.

## When to Use Gitea Workflows

Use this configuration only if:
1. You're running a self-hosted Gitea instance
2. You need to deploy to a specific VPS via SSH
3. You're NOT using GitHub Actions for VPS deployments

## Avoiding Redundant Deployments

⚠️ **WARNING:** If this repository is mirrored to Gitea AND GitHub simultaneously, pushes will trigger multiple concurrent deployments, causing race conditions.

**Recommendation:** Choose ONE of the following:
- GitHub Actions (for cloud deployments and general CI/CD)
- Gitea Workflows (for self-hosted VPS deployments only)

## Disabling Gitea Workflows

To disable this configuration:

```bash
# Rename to prevent Gitea from detecting it
mv .gitea/workflows/deploy-vps.yml .gitea/workflows/deploy-vps.yml.disabled
```

Or remove the workflow file entirely if not needed:

```bash
rm .gitea/workflows/deploy-vps.yml
```

## Required Secrets

If you choose to use Gitea workflows, configure these secrets in your Gitea repository settings:
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_TOKEN` - Docker Hub access token
- `VPS_HOST` - VPS IP address or hostname
- `VPS_USERNAME` - SSH username
- `VPS_SSH_KEY` - SSH private key for authentication
- `VPS_PORT` - SSH port (usually 22)
- `TELEGRAM_CHAT_ID` - Telegram chat ID for notifications
- `TELEGRAM_TOKEN` - Telegram bot token

## VPS Requirements

Your VPS must have:
1. Docker and docker-compose installed
2. SSH access configured
3. Git installed
4. Sufficient resources to run the application

## More Information

For deployment strategy and best practices, see [DEPLOYMENT_STRATEGY.md](../../DEPLOYMENT_STRATEGY.md).
