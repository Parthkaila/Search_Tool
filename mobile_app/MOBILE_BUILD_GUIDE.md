# Mobile Application Setup Guide

## Architecture Overview

**Mobile App (Android)** ➜ **API Server (Cloud/PC)** ➜ **Google Maps Scraping**

- **Mobile App**: Kivy-based Android APK with full internet permissions
- **API Server**: FastAPI backend that does the actual Chrome scraping
- **Why this design**: Mobile devices cannot run Chrome automation, so scraping happens on server

---

## Part 1: Deploy API Server (Required First)

### Option A: Deploy on Render.com (Free)

1. **Create API Dockerfile**:
   Already created as `Dockerfile` in root folder (works for API server)

2. **Push to GitHub**:
   ```bash
   cd "d:\Python Word Dox Formating Software\mobile_app"
   git init
   git add .
   git commit -m "Maps scraper API"
   git push origin main
   ```

3. **Deploy on Render**:
   - Go to https://render.com
   - Create "Web Service" from repo
   - Select `api_server.py` as start command
   - Wait for deployment
   - **Copy your API URL**: `https://your-api.onrender.com`

### Option B: Run on Your PC (Testing)

```powershell
cd "d:\Python Word Dox Formating Software\mobile_app"
pip install -r api_requirements.txt
python api_server.py
```

Your API will run at: `http://localhost:8000`
To access from mobile on same WiFi: `http://YOUR_PC_IP:8000`

---

## Part 2: Build Android APK

### Prerequisites

1. **Install WSL2 on Windows**:
   ```powershell
   wsl --install
   ```

2. **In WSL Ubuntu, install dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip
   pip3 install buildozer cython
   ```

3. **Android SDK will auto-download** (first build takes 30+ min)

### Build APK

```bash
cd /mnt/d/Python\ Word\ Dox\ Formating\ Software/mobile_app
buildozer android debug
```

**Output**: `bin/GoogleMapsCollector-1.0-arm64-v8a-debug.apk`

### Install on Android

1. **Transfer APK to phone** via USB or cloud
2. **Enable "Install from unknown sources"** in Settings
3. **Install the APK**
4. **Grant all permissions** (Internet, Storage, etc.)

---

## Part 3: Configure Mobile App

1. **Open the app** on your Android device
2. **Enter Server URL**: 
   - If API on Render: `https://your-api.onrender.com`
   - If API on PC (same WiFi): `http://192.168.1.26:8000`
3. **Enter keywords**, location, max results
4. **Click "Collect Data"**
5. **Export to Excel** when done → Saves to Downloads folder

---

## Android Permissions (Auto-requested)

The app requests these permissions on first launch:
- ✅ `INTERNET` - Connect to API server
- ✅ `WRITE_EXTERNAL_STORAGE` - Save Excel files
- ✅ `READ_EXTERNAL_STORAGE` - Access downloads
- ✅ `ACCESS_NETWORK_STATE` - Check connection status

All configured in `buildozer.spec` and auto-requested via `android.permissions` in Python code.

---

## Quick Test Without Building APK

Use **Kivy Launcher** app from Play Store:
1. Install "Kivy Launcher" from Google Play
2. Copy `main.py` and `requirements.txt` to phone storage
3. Run through Kivy Launcher

---

## Production Release (Play Store)

For Google Play release:

```bash
buildozer android release
```

Then sign the APK with your keystore and upload to Play Console.

---

## Troubleshooting

**Build fails in WSL**:
- Make sure Java 17 is installed: `java -version`
- Clear buildozer cache: `buildozer android clean`

**App crashes on launch**:
- Check logcat: `adb logcat | grep python`
- Verify all permissions granted in Android settings

**Cannot connect to server**:
- Verify server URL is correct and accessible
- Check mobile device has internet connection
- If using PC IP, ensure both on same WiFi

**Excel export fails**:
- Grant storage permissions in Android settings
- Check Downloads folder: `/storage/emulated/0/Download/`

---

## File Structure

```
mobile_app/
├── main.py              # Kivy Android app
├── api_server.py        # FastAPI scraping backend
├── buildozer.spec       # Android build config
├── requirements.txt     # Mobile app dependencies
└── api_requirements.txt # API server dependencies
```

---

## Alternative: Build on Linux Directly

If you have a Linux machine:

```bash
sudo apt install buildozer
cd mobile_app
buildozer android debug deploy run
```

This builds and installs directly to connected Android device.

---

## Summary

1. ✅ Deploy API server to Render.com (free)
2. ✅ Build APK using buildozer in WSL2
3. ✅ Install APK on Android device
4. ✅ Grant permissions
5. ✅ Enter server URL in app
6. ✅ Collect data and export Excel

Your mobile app is now ready with **full internet permissions** and **cloud-based scraping**!
