# 🎯 Quick Start - Deploy to GitHub & Share with Friend

## Step-by-Step (5 minutes)

### Step 1: Prepare Your Code for GitHub

**Windows:**
```bash
setup_github.bat
```

**Mac/Linux:**
```bash
chmod +x setup_github.sh
./setup_github.sh
```

This will:
- ✅ Initialize Git
- ✅ Add all files
- ✅ Create first commit

---

### Step 2: Create GitHub Repository

1. Go to: **https://github.com/new**
2. **Repository name:** `documentation-analyzer`
3. **Make it PUBLIC** (so your friend can access)
4. **Don't** initialize with README (we already have files)
5. Click **"Create repository"**

---

### Step 3: Push Your Code

Copy the commands GitHub shows you, or use these (replace `YOUR_USERNAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/documentation-analyzer.git
git branch -M main
git push -u origin main
```

---

### Step 4: Deploy (Choose ONE)

#### 🚀 Option A: Render.com (Recommended - Permanent URL)

1. Go to: **https://render.com**
2. Sign up (free)
3. Click **"New +"** → **"Web Service"**
4. **Connect GitHub** → Select your repo
5. Configure:
   - **Name:** `doc-analyzer`
   - **Build Command:**
     ```
     pip install -r moengage_project/codebase/requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - **Start Command:**
     ```
     cd moengage_project/codebase && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
     ```
6. Click **"Create Web Service"**
7. Wait 5-10 minutes
8. **Copy your URL:** `https://doc-analyzer.onrender.com`

#### 🎮 Option B: GitHub Codespaces (Run in Browser)

1. Go to your GitHub repository
2. Click **"Code"** → **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. Wait 2-3 minutes
5. In terminal, run:
   ```bash
   cd moengage_project/codebase
   python app.py
   ```
6. Click **"Ports"** tab → Right-click port 5000 → **"Port Visibility"** → **"Public"**
7. **Copy the public URL** and share it!

---

### Step 5: Share with Your Friend! 🎉

Send them the URL:
- Render: `https://doc-analyzer.onrender.com`
- Codespaces: `https://xxxx-5000.preview.app.github.dev`

---

## What Your Friend Will See

✅ Beautiful web interface  
✅ Input field for any website URL  
✅ Analysis results in 3 tabs  
✅ Works on any device with a browser  

---

## Troubleshooting

**Git push fails?**
- Make sure you're logged in: `git config --global user.name "Your Name"`
- Check repository URL is correct

**Render deployment fails?**
- Check build logs in Render dashboard
- Make sure all files were pushed to GitHub

**Codespaces not working?**
- Make sure repository is Public
- Check port 5000 is forwarded

---

## Need More Help?

See `GITHUB_DEPLOYMENT.md` for detailed instructions.

