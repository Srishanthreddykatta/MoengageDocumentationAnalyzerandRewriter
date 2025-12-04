# 🚀 Quick Deployment Guide - Share with US Colleague

## Fastest Method: ngrok (5 minutes)

### Step 1: Test Locally
```bash
test_local.bat
```
Wait until you see: "Running on http://0.0.0.0:5000"

### Step 2: Get Public URL with ngrok

**Download ngrok:**
- Windows: `winget install ngrok` or download from https://ngrok.com/download
- Mac: `brew install ngrok`

**Start ngrok:**
```bash
ngrok http 5000
```

**Copy the URL:**
- You'll see: `Forwarding https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:5000`
- **Send this URL to your colleague!**

### Step 3: Share the URL
Send the ngrok URL (e.g., `https://abc123.ngrok-free.app`) to your US colleague.

---

## Permanent Method: Render.com (Free, 10 minutes)

### Step 1: Create Account
1. Go to https://render.com
2. Sign up (free)

### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repo OR upload files manually
3. Configure:
   - **Name:** doc-analyzer
   - **Build Command:**
     ```
     pip install -r moengage_project/codebase/requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - **Start Command:**
     ```
     cd moengage_project/codebase && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 300 app:app
     ```
4. Click "Create Web Service"
5. Wait 5-10 minutes for first deployment
6. Get your URL: `https://doc-analyzer.onrender.com`

### Step 3: Share
Send the Render URL to your colleague - it's permanent!

---

## One-Click Local + ngrok (Windows)

Just run:
```bash
deploy_local.bat
```

This will:
1. ✅ Start Flask app
2. ✅ Start ngrok automatically
3. ✅ Show you the public URL

---

## What Your Colleague Will See

1. A beautiful web interface
2. Input field for any website URL
3. "Analyze" button
4. Results in 3 tabs:
   - Analysis Report (readable format)
   - JSON Data (structured data)
   - Revised Content (improved version)

---

## Troubleshooting

**App won't start?**
- Run `test_local.bat` first to check for errors
- Make sure Python 3.11+ is installed

**ngrok not working?**
- Check firewall allows port 5000
- Try: `ngrok http 5000 --region us`

**Need help?**
- Check `DEPLOYMENT_GUIDE.md` for detailed instructions

---

## Recommended: Use Render.com

✅ Free forever (with limits)
✅ Permanent URL
✅ No need to keep your computer on
✅ Professional deployment

**Time:** 10 minutes setup, then permanent!

