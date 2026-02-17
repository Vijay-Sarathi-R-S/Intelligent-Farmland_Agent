# GitHub Actions Secrets Configuration

This document outlines the secrets required for the CI/CD pipelines.

## Step 1: Generate Docker Hub Access Token

1. Go to [Docker Hub Settings](https://hub.docker.com/settings/security)
2. Click "New Access Token"
3. Give it a name: `github-actions`
4. Select read/write permissions
5. Click "Generate"
6. Copy the token (you won't see it again!)

## Step 2: Add Secrets to GitHub

Using GitHub UI:
1. Go to Your Repository → Settings → Secrets and Variables → Actions
2. Click "New repository secret"
3. Add each secret below

Using GitHub CLI:
```bash
gh secret set DOCKER_USERNAME -b "your-docker-username"
gh secret set DOCKER_PASSWORD -b "your-docker-access-token"
gh secret set DEPLOYMENT_WEBHOOK_URL -b "https://example.com/webhook"  # Optional
```

## Required Secrets

### DOCKER_USERNAME
- **Value**: Your Docker Hub username
- **Used by**: CD workflow
- **Purpose**: Login to Docker Hub for image push

### DOCKER_PASSWORD
- **Value**: Docker Hub access token (NOT your password)
- **Used by**: CD workflow
- **Purpose**: Authenticate to Docker Hub

### DEPLOYMENT_WEBHOOK_URL (Optional)
- **Value**: Your deployment service webhook URL
- **Used by**: CD workflow deployment job
- **Purpose**: Trigger deployment on production servers
- **Example**: `https://your-deploy-service.com/webhooks/deploy`

## Environment Variables for Workflows

For API keys needed during CI/CD, either:

1. **Option A**: Add as repository secrets (requires secret masking)
```bash
gh secret set GEMINI_API_KEY -b "your-key"
gh secret set NASA_API_KEY -b "your-key"
```

Then reference in workflows:
```yaml
env:
  GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  NASA_API_KEY: ${{ secrets.NASA_API_KEY }}
```

2. **Option B**: Use .env.example as base (recommended)
- Keep .env file in .gitignore
- API keys only needed at runtime, not build time

## Testing Secrets Configuration

```bash
# List all secrets (shows names only, not values)
gh secret list

# Verify Docker login works
echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

# Test API connectivity
curl -H "X-API-Key: $GEMINI_API_KEY" https://api.example.com/test
```

## Security Best Practices

✅ **DO:**
- Use access tokens instead of passwords
- Rotate tokens regularly
- Use GitHub's secret masking
- Review workflow logs for accidental exposure
- Use branch protection rules
- Enable CODEOWNERS for workflow changes

❌ **DON'T:**
- Commit secrets to repository
- Share tokens via email or chat
- Use personal passwords
- Log secrets in workflow output
- Grant more permissions than needed

## Troubleshooting

### "Authentication server did not return a valid token"
- Check your Docker Hub token is current
- Regenerate token if necessary
- Verify username matches

### "Workflow failing on secret access"
- Ensure secret name matches exactly (case-sensitive)
- Check secret is available to repo (not limited to specific workflows)
- Verify runner has access to secrets

### "Image push denied"
- Verify Docker credentials are correct
- Check repository name is lowercase
- Ensure token has read/write permissions
