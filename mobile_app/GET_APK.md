# 🚀 Easy APK Build - No Setup Required!

## Get Your APK in 3 Steps (10 minutes)

### Step 1: Push Code to GitHub

```powershell
cd "d:\Python Word Dox Formating Software"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Google Maps Collector Mobile App"

# Create repo on GitHub first at: https://github.com/new
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: GitHub Builds APK Automatically

Once you push, GitHub Actions will:
- ✅ Automatically detect the workflow
- ✅ Build the Android APK (takes ~20-30 minutes)
- ✅ Create a release with downloadable APK

**Watch the build**:
- Go to your GitHub repo
- Click "Actions" tab
- See "Build Android APK" workflow running

### Step 3: Download APK

**Option A - From Artifacts** (Fastest):
1. Go to repo → Actions → Click the completed workflow run
2. Scroll down to "Artifacts"
3. Download "google-maps-collector-apk.zip"
4. Extract to get the APK file

**Option B - From Releases**:
1. Go to repo → Releases
2. Download the APK from latest release

### Step 4: Install on Your Phone

1. **Send APK to phone** via:
   - USB cable
   - WhatsApp/Telegram
   - Google Drive/Dropbox
   - Email
   - Direct download from GitHub on phone

2. **Enable "Install from Unknown Sources"**:
   - Settings → Security
   - Enable "Unknown Sources" or "Install Unknown Apps"

3. **Install the APK**:
   - Open the APK file
   - Click "Install"
   - Grant permissions (Internet, Storage)

4. **Open the app**:
   - Find "Google Maps Collector" in your apps
   - Open it
   - Enter server URL
   - Start collecting!

---

## Alternative: Build Locally (Advanced)

If you want to build yourself:

### On Windows with WSL2:

```powershell
# Install WSL2
wsl --install

# Restart PC, then in WSL Ubuntu:
cd /mnt/d/Python\ Word\ Dox\ Formating\ Software/mobile_app
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip
pip3 install buildozer cython
buildozer android debug

# APK will be in: bin/GoogleMapsCollector-1.0-arm64-v8a-debug.apk
```

### On Linux:

```bash
cd mobile_app
sudo apt install buildozer
buildozer android debug
```

---

## Troubleshooting

**GitHub Actions failing?**
- Check the Actions tab for error logs
- Make sure `mobile_app` folder exists in repo
- Verify `buildozer.spec` is in `mobile_app/`

**APK won't install?**
- Enable "Install from Unknown Sources"
- Make sure Android version is 5.0+ (API 21+)
- Download the APK again if corrupted

**App crashes?**
- Grant all permissions in Settings → Apps → Google Maps Collector
- Make sure you entered the correct server URL
- Check internet connection

---

## What Happens After GitHub Build?

✅ APK file name: `GoogleMapsCollector-1.0-arm64-v8a-debug.apk`
✅ Size: ~20-30 MB
✅ Works on: Android 5.0+ (most phones)
✅ Permissions: Auto-requested (Internet, Storage)
✅ Ready to install: No signing needed for debug APK

---

## Quick Summary

```
Push to GitHub → Wait 20-30 min → Download APK → Send to Phone → Install → Use!
```

**No Linux/WSL needed!** GitHub builds everything for you automatically.

---

## Need Help?

1. **First build takes 20-30 minutes** (GitHub downloads Android SDK)
2. **Subsequent builds are faster** (~10-15 minutes)
3. **Free on GitHub** (2000 minutes/month free tier)
4. **APK stays for 30 days** in artifacts

Your mobile app is ready to build! Just push to GitHub and wait for the magic ✨
