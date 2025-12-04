# Deployment Guide - Make Your App Accessible Worldwide

This guide will help you deploy the Documentation Analyzer so your foreign colleague in the US can access it.

## Option 1: Quick Local Access with ngrok (Fastest - 5 minutes)

This creates a temporary public URL that tunnels to your local machine.

### Steps:

1. **Download ngrok:**
   - Visit: https://ngrok.com/download
   - Or use: `winget install ngrok` (Windows) or `brew install ngrok` (Mac)

2. **Start your local app:**
   ```bash
   cd moengage_project/codebase
   python app.py
   ```
   Wait until you see: "Running on http://0.0.0.0:5000"

3. **In a NEW terminal, start ngrok:**
   ```bash
   ngrok http 5000
   ```

4. **Copy the forwarding URL:**
   - You'll see something like: `https://abc123.ngrok-free.app`
   - **Send this URL to your colleague!**

5. **Note:** Free ngrok URLs expire after 2 hours. For permanent access, use Option 2 or 3.

---

## Option 2: Deploy to Render (Free, Permanent URL)

### Steps:

1. **Create account:** Go to https://render.com and sign up (free)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or upload files)

3. **Configure:**
   - **Name:** doc-analyzer
   - **Environment:** Python 3
   - **Build Command:** 
     ```bash
     pip install -r moengage_project/codebase/requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - **Start Command:**
     ```bash
     cd moengage_project/codebase && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
     ```
   - **Plan:** Free

4. **Deploy:** Click "Create Web Service"

5. **Get your URL:** Render will give you a URL like `https://doc-analyzer.onrender.com`

---

## Option 3: Deploy to Railway (Free Trial, Easy Setup)

### Steps:

1. **Create account:** Go to https://railway.app and sign up

2. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

3. **Configure:**
   - Add `railway.json` file (already created)
   - Railway auto-detects Python and runs the build

4. **Get your URL:** Railway provides a URL like `https://your-app.railway.app`

---

## Option 4: Deploy to Heroku (Classic Option)

### Steps:

1. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create doc-analyzer-yourname
   ```

4. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Get URL:** `https://doc-analyzer-yourname.herokuapp.com`

---

## Testing Locally First

Before deploying, test locally:

```bash
cd moengage_project/codebase
pip install -r requirements.txt
playwright install chromium
python app.py
```

Then open: http://localhost:5000

---

## Recommended: Render (Easiest Free Option)

1. Sign up at render.com
2. Connect GitHub repo
3. Use the `render.yaml` file (already created)
4. Deploy - get permanent URL
5. Share URL with your colleague

**Render gives you:**
- ✅ Free tier (with some limits)
- ✅ Permanent URL
- ✅ Auto-deploy from GitHub
- ✅ Easy setup

---

## Quick Start Script

I've created `deploy_local.bat` (Windows) and `deploy_local.sh` (Linux/Mac) to help you start locally with ngrok automatically.

### Windows:
```bash
deploy_local.bat
```

### Linux/Mac:
```bash
chmod +x deploy_local.sh
./deploy_local.sh
```

This will:
1. Start your Flask app
2. Start ngrok automatically
3. Show you the public URL

---

## Important Notes

- **API Key:** Already configured, no changes needed
- **Port:** Default is 5000, but cloud platforms use `$PORT` environment variable
- **Playwright:** Needs to install browsers on first deploy (takes 2-3 minutes)
- **Timeout:** Analysis can take 1-2 minutes, so timeout is set to 300 seconds

---

## Troubleshooting

**If ngrok doesn't work:**
- Make sure port 5000 is not blocked by firewall
- Try: `ngrok http 5000 --region us` (US region)

**If Render/Railway fails:**
- Check build logs for errors
- Make sure `requirements.txt` is correct
- Playwright installation might take time

**If app doesn't start:**
- Check that all dependencies are in `requirements.txt`
- Verify Python version is 3.11+

