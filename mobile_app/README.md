# Google Maps Mobile Application

Complete mobile app solution with Android APK + cloud API backend.

## 📱 What You Get

- **Android APK**: Installable mobile app with full internet permissions
- **API Backend**: FastAPI server for Google Maps scraping (runs on cloud/PC)
- **Excel Export**: Save collected data directly to phone's Downloads folder
- **Filters**: Remove duplicates, remove entries without phone numbers
- **Stop/Resume**: Stop collection anytime and keep partial data

## 🚀 Quick Start

### 1. Deploy API Server (5 minutes)

**Easiest: Render.com (Free)**
```bash
# Push mobile_app folder to GitHub
git init
git add .
git commit -m "Maps API"
git push origin main

# Deploy on Render.com
# - Go to render.com
# - New Web Service from repo
# - Will auto-detect Dockerfile
# - Copy your URL: https://your-api.onrender.com
```

### 2. Get APK (NO SETUP REQUIRED! ✨)

**Easiest Way - GitHub Auto-Build:**

Just push to GitHub and it builds APK automatically! See [GET_APK.md](GET_APK.md)

```bash
# Push code to GitHub
git push origin main

# Wait 20-30 minutes
# GitHub Actions builds APK automatically

# Download from:
# Repo → Actions → Latest run → Artifacts → Download APK
# OR
# Repo → Releases → Download APK
```

**Alternative - Manual Build on Windows with WSL2:**
```bash
# In WSL Ubuntu terminal
cd /mnt/d/Python\ Word\ Dox\ Formating\ Software/mobile_app
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip
pip3 install buildozer cython
buildozer android debug
```

**Output**: `bin/GoogleMapsCollector-1.0-arm64-v8a-debug.apk`

### 3. Install on Android

1. Transfer APK to phone
2. Enable "Install from unknown sources"
3. Install APK
4. Grant permissions (Internet, Storage)

### 4. Use the App

1. Open app
2. Enter server URL: `https://your-api.onrender.com`
3. Enter keywords, location, max results
4. Click "Collect Data"
5. Export to Excel (saves to Downloads)

## 📁 Files

- `main.py` - Kivy Android app UI
- `api_server.py` - FastAPI scraping backend
- `buildozer.spec` - Android build configuration
- `Dockerfile` - Container for API server
- `render.yaml` - Render.com deploy config
- `requirements.txt` - Mobile app dependencies
- `api_requirements.txt` - API server dependencies
- `MOBILE_BUILD_GUIDE.md` - Complete build instructions

## 🔐 Android Permissions (All Granted)

✅ `INTERNET` - Connect to API server
✅ `WRITE_EXTERNAL_STORAGE` - Save Excel files
✅ `READ_EXTERNAL_STORAGE` - Access downloads
✅ `ACCESS_NETWORK_STATE` - Check connectivity

Configured in `buildozer.spec` and auto-requested on app launch.

## 🏗️ Architecture

```
┌─────────────┐        ┌──────────────┐        ┌──────────────┐
│   Android   │  HTTP  │  API Server  │  WEB   │ Google Maps  │
│   Mobile    │ ─────► │  (FastAPI)   │ ─────► │   Scraping   │
│     App     │        │  on Cloud    │        │              │
└─────────────┘        └──────────────┘        └──────────────┘
```

Mobile cannot run Chrome automation → API server does scraping → Returns data to mobile

## 📝 Complete Guide

See [MOBILE_BUILD_GUIDE.md](MOBILE_BUILD_GUIDE.md) for detailed instructions including:
- Prerequisites setup
- Building APK on Windows/Linux
- Deploying API to multiple cloud platforms
- Troubleshooting common issues
- Play Store release steps

## 🎯 Features

- ✅ Native Android APK
- ✅ Full internet permissions
- ✅ Cloud-based scraping (no mobile Chrome needed)
- ✅ Export to Excel (.xlsx)
- ✅ Stop collection anytime
- ✅ Duplicate removal
- ✅ Filter by phone availability
- ✅ Progress tracking
- ✅ Works offline (after data collected)

## 🆓 Free Hosting

API server can be hosted FREE on:
- Render.com (750 hrs/month)
- Railway.app ($5 credits/month)
- Google Cloud Run (2M requests/month)
- Fly.io (3 VMs free)

## 🔧 Development

Test without building APK:
```bash
# Install Kivy Launcher from Play Store
# Copy main.py to phone storage
# Run from Kivy Launcher
```

Build release APK for Play Store:
```bash
buildozer android release
# Then sign with keystore
```

---

**Your mobile app with full internet permissions is ready!**
