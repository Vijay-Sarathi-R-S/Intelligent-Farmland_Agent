# Render Deployment Quick Start

## 5-Minute Deploy Guide

### Step 1: Prepare Repository
```
git status
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub

### Step 3: Deploy Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select this repository
4. Configure:
   - Name: `agritech`
   - Environment: `Docker`
   - Plan: `Free`
5. Click "Create Web Service"

### Step 4: Add Environment Variables
In Render Dashboard → Environment tab, add:

```
FLASK_ENV=production
PYTHONUNBUFFERED=1
GEMINI_API_KEY=your-key
NASA_API_KEY=your-key
SECRET_KEY=random-secure-string
```

### Step 5: Deploy
Render automatically builds and deploys! 
Your app will be live at: https://agritech.onrender.com

---

## ⚠️ Free Tier Limits
- Sleeps after 15 min inactivity (30s to wake)
- 512 MB RAM, 1 shared CPU
- 100 GB/month bandwidth
- Upgrade to $7/month for no sleep & auto-scaling

---

## 📚 Documentation
- Full guide: DEPLOYMENT.md
- File reference: RENDER_FILES_SUMMARY.md
