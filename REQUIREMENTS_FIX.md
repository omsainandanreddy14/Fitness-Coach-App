# 🔧 Requirements Installation Fix

## Problem: "Error installing requirements" on Streamlit Cloud

This happens when packages fail to compile or install due to dependency issues.

---

## ✅ Solution Applied

I've updated both files for maximum compatibility on Streamlit Cloud:

### 1. **requirements.txt** - Pinned Specific Versions
```
streamlit==1.32.2
opencv-python-headless==4.8.1.78  # Specific working version
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
mediapipe==0.10.8
google-generativeai==0.3.0
protobuf==3.20.0
requests==2.31.0
```

### 2. **packages.txt** - Complete System Dependencies
Added build-essential and all required libraries for compilation:
```
ffmpeg
libsm6
libxext6
libxrender-dev
libgomp1
libglib2.0-0
libxkbcommon-x11-0
libdbus-1-3
libgl1-mesa-glx
libegl1-mesa
libxkbcommon0
python3-dev
build-essential
```

---

## 🚀 Redeploy Steps

### Option 1: Force Fresh Deploy (Recommended)

```bash
# In PowerShell in your project folder:
git add .
git commit -m "Fix: Pinned versions for Streamlit Cloud compatibility"
git push origin main
```

Then:
1. Go to https://share.streamlit.io
2. Find your app
3. Click **"..."** (top right) → **"Manage app"**
4. Click **"Reboot app"** or let it auto-deploy
5. Wait **5-10 minutes** for full build

### Option 2: Delete & Redeploy Fresh

If reboot doesn't work:
1. Click **"..."** → **"Settings"** → **"Delete app"**
2. Go to https://share.streamlit.io → **"New app"**
3. Select your GitHub repo again
4. Fresh install will use new dependencies

---

## 📋 Troubleshooting Checklist

Before redeploying, verify:

- [ ] `requirements.txt` exists (not `requirement.txt`)
- [ ] `packages.txt` exists in root directory
- [ ] All files committed to GitHub
- [ ] Repository is **PUBLIC** 
- [ ] Branch is `main` or `master`
- [ ] No uncommitted changes

Check with:
```bash
git status
git log --oneline
```

---

## 🔍 Check Deployment Status

1. Go to your app on **https://share.streamlit.io**
2. Click **"Manage app"** (lower right)
3. Check **"Logs"** tab for errors
4. Look for specific package failures

Common log messages:
- ✅ "Successfully installed" = Good!
- ❌ "error: command 'gcc' failed" = Build issue
- ❌ "No module named" = Missing dependency

---

## 🎯 Alternative: Minimal Requirements

If issues persist, try minimal version:

```
streamlit==1.32.2
opencv-python-headless==4.8.1.78
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
mediapipe==0.10.8
google-generativeai==0.3.0
```

Remove:
- protobuf (usually bundled)
- requests (usually pre-installed)

---

## ✨ After Successful Deploy

You'll see:
1. ✅ Green checkmark on app status
2. ✅ App loads without errors
3. ✅ Can access all features:
   - BMR Calculator
   - Video Upload
   - WebCam Mode
   - Diet Plan Generator

---

## 🆘 Still Having Issues?

### Check Logs Directly:
```bash
# If using command line deployment:
streamlit logs
```

### Community Help:
- Streamlit Issues: https://github.com/streamlit/streamlit/issues
- Streamlit Forum: https://discuss.streamlit.io
- Stack Overflow: Tag `streamlit` + `opencv`

### Report Package Issue:
Include in your post:
- Error message from logs
- Operating system of your machine
- Python version
- Exact requirements.txt content

---

## 📚 Related Files

- **DEPLOYMENT.md** - Main deployment guide
- **README.md** - App documentation
- **.gitignore** - Excludes secrets from repo
- **.streamlit/config.toml** - Streamlit settings
- **.streamlit/secrets.toml** - API keys (never commit!)

---

## 🎉 Success!

Once deployed, your app URL is:
```
https://your-username-fitness-coach-app.streamlit.app
```

All features ready to use! 🚀

---

**Last Updated:** March 18, 2026
**Status:** ✅ Optimized for Streamlit Cloud
