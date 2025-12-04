# 🚀 Deploy to GitHub - Share with Your Friend

## Option 1: GitHub Codespaces (Easiest - Run Directly from GitHub!)

This lets you run the app in the cloud and share access with your friend.

### Step 1: Push Code to GitHub

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it: `documentation-analyzer`
   - Make it **Public** (so your friend can access)
   - Click "Create repository"

2. **Push your code:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Documentation Analyzer"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/documentation-analyzer.git
   git push -u origin main
   ```

### Step 2: Open in Codespaces

1. **Go to your repository on GitHub**
2. **Click the green "Code" button**
3. **Click "Codespaces" tab**
4. **Click "Create codespace on main"**
5. **Wait 2-3 minutes for setup**

### Step 3: Run the App

Once Codespaces opens:

```bash
cd moengage_project/codebase
python app.py
```

### Step 4: Share with Your Friend

1. **Click the "Ports" tab** in VS Code (bottom panel)
2. **Right-click on port 5000** → "Port Visibility" → "Public"
3. **Copy the public URL** (e.g., `https://xxxx-5000.preview.app.github.dev`)
4. **Share this URL with your friend!**

**OR** use the share button in Codespaces to invite your friend directly!

---

## Option 2: Deploy to Render (Auto-Deploy from GitHub)

This gives you a permanent URL that auto-updates when you push to GitHub.

### Step 1: Push to GitHub (Same as above)

### Step 2: Deploy on Render

1. **Go to https://render.com**
2. **Sign up/Login** (free)
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub account**
5. **Select your repository:** `documentation-analyzer`
6. **Configure:**
   - **Name:** `doc-analyzer`
   - **Environment:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r moengage_project/codebase/requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - **Start Command:**
     ```bash
     cd moengage_project/codebase && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
     ```
   - **Plan:** Free
7. **Click "Create Web Service"**
8. **Wait 5-10 minutes** for first deployment
9. **Get your URL:** `https://doc-analyzer.onrender.com`

### Step 3: Share the URL

Send the Render URL to your friend - it's permanent and auto-updates!

---

## Option 3: Railway (Also Auto-Deploys from GitHub)

### Step 1: Push to GitHub (Same as above)

### Step 2: Deploy on Railway

1. **Go to https://railway.app**
2. **Sign up** (free trial)
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Railway auto-detects settings** (uses `railway.json`)
7. **Get your URL:** `https://your-app.railway.app`

---

## Quick Comparison

| Method | Setup Time | Cost | Permanent URL | Auto-Update |
|-------|-----------|------|---------------|-------------|
| **Codespaces** | 5 min | Free (limited hours) | ✅ Yes | ❌ No |
| **Render** | 10 min | Free | ✅ Yes | ✅ Yes |
| **Railway** | 5 min | Free trial | ✅ Yes | ✅ Yes |

---

## Recommended: Render.com

✅ **Free forever** (with limits)  
✅ **Permanent URL**  
✅ **Auto-deploys** when you push to GitHub  
✅ **Professional** - looks great for sharing  

**Steps:**
1. Push code to GitHub
2. Connect to Render
3. Deploy (one click)
4. Share URL with friend
5. Done!

---

## What Your Friend Will See

Once deployed, your friend can:
- ✅ Access the web interface
- ✅ Enter any website URL
- ✅ Get analysis results
- ✅ View in 3 different formats

---

## Troubleshooting

**Codespaces not working?**
- Make sure repository is Public
- Check port 5000 is forwarded
- Try restarting the codespace

**Render deployment fails?**
- Check build logs
- Verify `requirements.txt` is correct
- Playwright installation takes 2-3 minutes

**Need help?**
- Check repository: Make sure all files are committed
- Check logs: Render/Railway show build logs
- Test locally first: `test_local.bat`

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Push your code
3. ✅ Choose deployment method (Render recommended)
4. ✅ Share URL with friend
5. ✅ Done!

