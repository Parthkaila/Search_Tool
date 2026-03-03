# Git Setup and Deploy to GitHub

## Quick Push to GitHub

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it: `google-maps-scraper` (or your choice)
   - Make it Public
   - Don't initialize with README (we already have files)
   - Click "Create repository"

2. **Push your code**
   ```powershell
   cd "d:\Python Word Dox Formating Software"
   git init
   git add .
   git commit -m "Google Maps data collector with filters"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/google-maps-scraper.git
   git push -u origin main
   ```

3. **Deploy on Render.com**
   - Go to https://render.com
   - Sign in with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Click "Create Web Service"
   - Wait 5-10 minutes
   - Your website is live!

Your website URL will be: `https://google-maps-scraper.onrender.com` (or your custom name)

## Notes
- Replace `YOUR_USERNAME` with your actual GitHub username
- The website works on all devices (mobile, tablet, PC)
- Free tier may sleep after 15min inactivity
- First access after sleep takes 30-60 seconds
