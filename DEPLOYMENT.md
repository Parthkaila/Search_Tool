# Free Website Hosting Guide

## ⚠️ Important Note
**InfinityFree does NOT support Python/Chrome automation.** Use these free platforms instead:

---

## Option 1: Render.com (Recommended) ⭐

**Free tier**: 750 hours/month, supports Docker + Chrome

### Steps:
1. **Push code to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Go to Render.com**
   - Sign up at https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

3. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for build
   - Your app will be live at: `https://your-app-name.onrender.com`

**Pros**: Free, reliable, auto-deploys on git push
**Cons**: Instance spins down after 15min inactivity (takes 30-60 sec to wake up)

---

## Option 2: Railway.app

**Free tier**: $5 credits/month (enough for ~500 hours)

### Steps:
1. **Push code to GitHub** (same as above)

2. **Go to Railway.app**
   - Sign up at https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will use `railway.json` config

3. **Deploy**
   - Railway builds automatically
   - Add domain in Settings → Networking
   - Your app will be live at: `https://your-app.up.railway.app`

**Pros**: Faster than Render, stays active longer
**Cons**: Free credits run out (need to upgrade after)

---

## Option 3: Google Cloud Run

**Free tier**: 2 million requests/month

### Steps:
1. **Install Google Cloud SDK**
   ```powershell
   # Download from https://cloud.google.com/sdk/docs/install
   ```

2. **Build and deploy**
   ```powershell
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/maps-scraper
   gcloud run deploy maps-scraper --image gcr.io/YOUR_PROJECT_ID/maps-scraper --platform managed --region us-central1 --allow-unauthenticated
   ```

3. **Access your app**
   - Google provides a URL like: `https://maps-scraper-xxxxx-uc.a.run.app`

**Pros**: Very generous free tier, scales automatically
**Cons**: More complex setup

---

## Option 4: Fly.io

**Free tier**: 3 shared-cpu VMs, 3GB RAM total

### Steps:
1. **Install Fly CLI**
   ```powershell
   pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```

2. **Launch app**
   ```powershell
   cd "d:\Python Word Dox Formating Software"
   fly launch
   fly deploy
   ```

3. **Access**
   - Your app will be at: `https://your-app.fly.dev`

**Pros**: Good free tier, fast deployment
**Cons**: Limited resources on free plan

---

## Quick Deploy to Render (Easiest)

1. **Create GitHub account** (if you don't have one)
2. **Upload your code to GitHub**
3. **Go to Render.com** and sign in with GitHub
4. **Click "New Web Service"** and select your repo
5. **Done!** Your website is live

---

## After Deployment

Your website will be accessible from **any device** (mobile, tablet, PC) worldwide at the provided URL.

**No need for**:
- Running Python on your PC
- Keeping terminal open
- Same WiFi network

**Note**: On free plans, apps may sleep after inactivity. First request takes 30-60 seconds to wake up.

---

## Recommended: Render.com

For this project, **Render.com** is the best choice:
- ✅ Free forever (750 hrs/month)
- ✅ Supports Chrome automation
- ✅ Auto-deploy from GitHub
- ✅ Simple setup (no credit card needed)
- ✅ HTTPS included
- ✅ Works on mobile perfectly

**Your website will be**: `https://your-chosen-name.onrender.com`
