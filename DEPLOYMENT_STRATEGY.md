# Deployment Strategy

## Overview
This document clarifies the deployment strategy for the GenX FX platform to prevent redundant deployments and optimize CI/CD workflows.

## Primary Deployment Platform

**GitHub Actions** is the primary CI/CD platform for this project.

### Active Workflows
- `ci-cd.yml`: Main CI/CD pipeline (tests, builds, deploys to staging/production)
- `deploy-static.yml`: Static site deployment to AWS S3/CloudFront
- `manual-deploy.yml`: Manual deployment trigger for specific environments
- `branch-cleanup.yml`: Weekly cleanup of merged branches

## Alternative Platforms (Optional)

### GitLab CI (`.gitlab-ci.yml`)
- **Status**: OPTIONAL - Only use if deploying via GitLab
- **Purpose**: Builds Docker images to Docker Hub (`keamouyleng/genx_docker`)
- **Recommendation**: Disable if not actively using GitLab

### Gitea (`.gitea/workflows/deploy-vps.yml`)
- **Status**: OPTIONAL - Only use for VPS deployments
- **Purpose**: Deploys to VPS via SSH with health checks
- **Recommendation**: Enable only if deploying to a specific VPS

### Google Cloud Build (`cloudbuild.yaml`, `cloudbuild.immediate.yaml`)
- **Status**: OPTIONAL - Only use if deploying to Google Cloud Run
- **Purpose**: Builds and deploys to Google Cloud Run
- **Recommendation**: Use only for Google Cloud deployments

## Avoiding Redundant Deployments

### Issue
Previously, pushing to `main` would trigger:
1. GitHub Actions CI/CD
2. GitLab CI build/push
3. Gitea VPS deployment
4. Google Cloud Build (if configured)

This caused race conditions and inconsistent deployments.

### Solution
**Choose ONE deployment platform** based on your infrastructure:

#### Option 1: GitHub Actions Only (Recommended)
1. Keep GitHub Actions workflows active
2. Rename `.gitlab-ci.yml` to `.gitlab-ci.yml.disabled`
3. Rename `.gitea/workflows/deploy-vps.yml` to `.gitea/workflows/deploy-vps.yml.disabled`
4. Use Google Cloud Build only if specifically needed

#### Option 2: GitLab CI Primary
1. Disable GitHub Actions deployment jobs (keep tests only)
2. Use `.gitlab-ci.yml` for builds and deployments
3. Disable Gitea workflows

#### Option 3: Multi-Environment
1. GitHub Actions: Main production deployments
2. Gitea: VPS-specific deployments (staging/testing)
3. GitLab CI: Disabled
4. Ensure deployment targets don't conflict

## Cleanup and Maintenance

### Automated Cleanup
- **Branch Cleanup**: Weekly (Sundays 2 AM UTC) - removes merged branches
- **Docker Registry Cleanup**: After production deployments - keeps last 10 versions
- **VPS Docker Cleanup**: During deployments - removes images older than 24 hours

### Manual Cleanup
If you need to manually clean up Docker images:

```bash
# GitHub Container Registry
gh api -X DELETE /users/{username}/packages/container/{package}/versions/{version_id}

# Docker Hub
docker rmi keamouyleng/genx_docker:old-tag

# VPS
ssh user@vps "docker system prune -af --filter 'until=24h'"
```

## Deployment Targets

### Production
- **Trigger**: Push to `main` branch
- **Platform**: GitHub Actions (ci-cd.yml)
- **Environment**: production

### Staging
- **Trigger**: Push to `develop` branch
- **Platform**: GitHub Actions (ci-cd.yml)
- **Environment**: staging

### Manual Deployment
- **Trigger**: Manual workflow dispatch
- **Platform**: manual-deploy.yml
- **Environments**: staging, production

### Static Site
- **Trigger**: Push to `main` with changes in `client/**`
- **Platform**: deploy-static.yml
- **Target**: AWS S3 + CloudFront

## Best Practices

1. **Single Source of Truth**: Use one primary CI/CD platform
2. **Branch Protection**: Require PR reviews before merging to main
3. **Environment Secrets**: Store all secrets in GitHub Secrets
4. **Health Checks**: Always verify deployments with health checks
5. **Rollback Strategy**: Keep last 10 images for quick rollback
6. **Monitoring**: Monitor deployment success/failure rates

## Troubleshooting

### Multiple Deployments Running
**Problem**: Several platforms deploying simultaneously
**Solution**: Disable unused CI/CD configurations by renaming files

### Branch Cleanup Failing
**Problem**: Permission denied when deleting branches
**Solution**: Fixed in updated `branch-cleanup.yml` with proper permissions

### Old Images Accumulating
**Problem**: Docker registry filling up
**Solution**: Automated cleanup job now runs after production deployments

### Deployment Conflicts
**Problem**: Different platforms deploying different versions
**Solution**: Choose and document one primary deployment platform

## Migration Guide

If you're currently using multiple platforms and want to consolidate:

1. **Audit Active Deployments**: Check which platforms are actually deploying
2. **Choose Primary Platform**: Select GitHub Actions, GitLab CI, or Gitea
3. **Disable Others**: Rename unused workflow files to `.disabled`
4. **Update Documentation**: Document your choice in README.md
5. **Test**: Perform test deployment to verify single-platform operation
6. **Monitor**: Watch for any deployment issues over the next week

## Questions?

If you're unsure which deployment platform to use, consider:
- **GitHub Actions**: Best for most projects, integrated with GitHub
- **GitLab CI**: Use if your team primarily uses GitLab
- **Gitea**: Use for self-hosted deployments to specific VPS
- **Google Cloud Build**: Use only if deploying to Google Cloud Run

For questions or issues, please open a GitHub issue with the `deployment` label.
