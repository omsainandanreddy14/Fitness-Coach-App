# 🚀 Deployment Guide - Fitness AI Coach

## Option 1: Streamlit Community Cloud (Recommended - FREE)

This is the easiest and most recommended way to deploy your app.

### Step-by-Step Deployment:

1. **Create a GitHub Account** (if you don't have one)
   - Visit https://github.com
   - Sign up for free

2. **Create a GitHub Repository**
   - Go to https://github.com/new
   - Repository name: `fitness-coach-app`
   - Description: "🏋️ Fitness AI Coach - AI-powered fitness tracking with computer vision"
   - Make it **Public**
   - Click "Create repository"

3. **Push Your Code to GitHub**
   
   Open PowerShell in your project directory and run:
   
   ```bash
   # Initialize git repository
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: Fitness AI Coach app"
   
   # Add remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
   git remote add origin https://github.com/YOUR_USERNAME/fitness-coach-app.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

4. **Deploy on Streamlit Community Cloud**
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account
   - Click "New app"
   - Fill in:
     - **GitHub repo**: `YOUR_USERNAME/fitness-coach-app`
     - **Branch**: `main`
     - **Main file path**: `main.py`
   - Click "Deploy"

5. **Add Your API Key**
   - After deployment, click on the "..." menu (top right)
   - Select "Settings"
   - Go to "Secrets" tab
   - Add your secrets:
   ```
   GEMINI_API_KEY = "your-api-key-here"
   ```
   - Save and the app will restart automatically

6. **Access Your App**
   - Your app will be live at: `https://YOUR_USERNAME-fitness-coach-app.streamlit.app`
   - Share this link with anyone!

---

## Option 2: Railway (Easy Alternative)

1. **Create Railway Account**
   - Visit https://railway.app
   - Sign up with GitHub
   
2. **Connect Repository**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your fitness-coach-app repository
   - Select Python as the service

3. **Add Environment Variables**
   - In Railway dashboard, go to "Variables"
   - Add: `GEMINI_API_KEY=your-api-key`

4. **Deploy**
   - Railway will automatically detect and run `streamlit run main.py`
   - Your app URL will be provided

---

## Option 3: Heroku (Traditional Hosting)

1. **Create Heroku Account** at https://www.heroku.com

2. **Install Heroku CLI**
   ```bash
   # Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
   # Or install via chocolatey:
   choco install heroku-cli
   ```

3. **Create Procfile**
   Create a file named `Procfile` (no extension) with:
   ```
   web: streamlit run main.py --logger.level=error --server.port=$PORT
   ```

4. **Deploy**
   ```bash
   heroku login
   heroku create your-fitness-app-name
   git push heroku main
   ```

---

## Important: Environment Variables & Secrets

Your `GEMINI_API_KEY` should NEVER be committed to GitHub. Deployment platforms provide secure ways to store secrets:

### Streamlit Cloud:
- Settings → Secrets tab
- Enter in format: `GEMINI_API_KEY = "your-key"`

### Railway:
- Project Settings → Variables
- Add environment variables

### Heroku:
- Click "Settings" → "Reveal Config Vars"
- Add `GEMINI_API_KEY` as key, your key as value

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'mediapipe'"
- This means requirements aren't installed properly
- Ensure `requirement.txt` has all dependencies
- Restart your deployment

### "GEMINI_API_KEY not found"
- Check you've added it to secrets properly
- Redeploy after adding the key
- Wait 2-3 minutes for changes to take effect

### App takes too long to load
- Free tier has limited resources
- First load may take 30-60 seconds
- Subsequent loads will be faster

### Video upload doesn't work
- Check file size (max 500MB)
- Use common formats: MP4, MOV, AVI, M4V
- Ensure good internet connection

---

## Performance Tips

1. **Cache data when possible** to reduce API calls
2. **Use WebCam Mode for real-time** (lighter than video mode)
3. **Optimize video resolution** before uploading
4. **Keep dependencies updated** but stable

---

## After Deployment

✅ Share your deployment link! Format:
- Streamlit: `https://your-username-fitness-coach-app.streamlit.app`
- Railway: `https://your-app-name-production.up.railway.app`
- Heroku: `https://your-fitness-app-name.herokuapp.com`

✅ Monitor usage in your deployment dashboard

✅ Keep your API key secure - never share it publicly

✅ Update your app by pushing new commits to GitHub (auto-deploys)

---

## Need Help?

- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Help**: https://docs.github.com
- **Google Gemini API**: https://ai.google.dev
- **Community Support**: https://discuss.streamlit.io

Happy deploying! 🚀
