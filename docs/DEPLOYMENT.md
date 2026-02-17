# Render Deployment Guide

## Option 1: One-Click Deploy (Recommended)

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub account
4. Select this repository
5. Configure:
   - Name: agritech
   - Environment: Docker
   - Branch: main
   - Plan: Free
6. Add Environment Variables:
   - FLASK_ENV=production
   - PYTHONUNBUFFERED=1
   - GEMINI_API_KEY=(your key)
   - NASA_API_KEY=(your key)
   - SECRET_KEY=(generate random string)
7. Click "Create Web Service"

Render will automatically build and deploy!

## Environment Variables Required

Set in Render dashboard:

```
FLASK_ENV=production
PYTHONUNBUFFERED=1
GEMINI_API_KEY=[your-gemini-key]
NASA_API_KEY=[your-nasa-key]
SECRET_KEY=[generate-random-secure-string]
```

## Render Free Tier Limitations

- Instance sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 512 MB RAM (app uses ~100-150MB)
- 1 shared CPU core
- 100 GB/month bandwidth
- Limited to 1 gunicorn worker

## Upgrade to Paid Plan

- $7/month for Starter Plan
- No sleep, auto-scaling, better performance

## Files Created/Updated

### New Files:
- render.yaml - Render configuration
- Procfile - Process specification
- .renderignore - Build exclusions
- docker-compose.render.yml - Render simulation
- .env.render.example - Environment template
- render-build.ps1 - Windows build script
- render-deploy.yml - GitHub Actions workflow
- Makefile - Convenience commands
- RENDER_QUICKSTART.md - Quick start guide

### Updated Files:
- Dockerfile - Optimized for Render (1 worker, health checks)
- docker-compose.yml - Added Render notes
- .github/workflows/docker-build.yml - Changed to Render API
- .github/workflows/ci.yml - Enhanced CI testing

## Troubleshooting

### Service won''t start?
- Check logs in Render dashboard
- Verify all environment variables are set
- Test locally: flask run

### Out of memory?
- Free tier has 512 MB limit
- App uses ~150MB normally
- Restart service from dashboard

### API rate limits?
- NASA free tier: 42 requests/hour
- Open-Meteo: 10,000 requests/day free

## Monitoring

1. **View logs**: Render Dashboard → Your service → Logs
2. **Set alerts**: Account Settings → Notifications
3. **Check metrics**: Activity tab shows CPU, Memory, Network

## Next Steps

1. Deploy following Option 1 above
2. Test at https://your-service-name.onrender.com
3. Monitor logs for first 24 hours
4. Set up notifications (if needed)
5. Plan upgrade if hitting free tier limits

## Support

- Render Docs: https://render.com/docs
- Discord: Render community support
