# Deployment Guide - College Canteen Application

This guide will help you deploy your College Canteen application to **Render**, making it accessible to anyone online.

## Prerequisites

Before deploying, ensure you have:
- A GitHub account (free at github.com)
- A Render account (free at render.com)
- Your application code pushed to GitHub

## Step 1: Push Code to GitHub

### 1a. Create a GitHub Repository

1. Go to [github.com](https://github.com) and log in
2. Click **"New"** button to create a new repository
3. Name it: `college-canteen` (or any name you prefer)
4. Choose **Public** (so you can access it from Render)
5. Click **"Create repository"**

### 1b. Push Your Code to GitHub

Open PowerShell in your project folder and run:

```powershell
# Initialize git (only first time)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: College Canteen application"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/college-canteen.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render

### 2a. Connect Render to GitHub

1. Go to [render.com](https://render.com)
2. Sign up and log in
3. Click **"New +"** button
4. Select **"Web Service"**
5. Click **"Connect a repository"**
6. Authorize Render to access your GitHub account
7. Select your `college-canteen` repository

### 2b. Configure the Web Service

Fill in the deployment configuration:

| Field | Value |
|-------|-------|
| **Name** | `college-canteen` |
| **Environment** | `Python 3` |
| **Region** | Select closest to your location |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |

### 2c: Add Environment Variables

After creating the service, go to **Settings** and add these variables:

```
SECRET_KEY = canteen-secret-key-generate-a-random-string-here
FLASK_ENV = production
```

**Important**: Replace the SECRET_KEY with a random string (use a generator tool or any random text)

### 2d: Deploy

Click **"Create Web Service"** and Render will automatically:
- Build your application
- Install dependencies
- Start the Flask server

**Wait 5-10 minutes for deployment** (watch the logs for progress)

## Step 3: Access Your Application

Once deployed successfully, Render will give you a URL like:
```
https://college-canteen-xxxx.onrender.com
```

### Login with Admin Credentials:
- **Username**: `admin`
- **Password**: `admin123`

## Step 4: Database Notes

⚠️ **IMPORTANT DATABASE CONSIDERATION**:

Your app currently uses **SQLite** (file-based database), which works fine but has limitations on cloud servers:
- Data may be lost on redeploy
- Not ideal for production with multiple users

### Recommended: Use PostgreSQL (Optional)

If you want persistent data:

1. **On Render Dashboard**:
   - Click **"New +"** → **"PostgreSQL"**
   - Create a free PostgreSQL database
   - Copy the database connection string

2. **Update `config.py`** in production mode:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host:5432/dbname'
```

3. **Add to Render environment variables**:
```
DATABASE_URL = (paste your Postgres connection string)
```

## Common Issues & Fixes

### ❌ Build Fails
- Check that `requirements.txt` includes all dependencies
- Ensure **Build Command** is: `pip install -r requirements.txt`
- View logs for specific errors

### ❌ Port Error
- Render automatically assigns a port via `$PORT` environment variable
- Make sure your `run.py` listens on `0.0.0.0` (not just localhost)

### ❌ Static Files Not Loading
- Render serves static files automatically from `/app/static`
- If issues persist, enable "Auto Deploy" and redeploy

### ❌ Database Not Working
- Use PostgreSQL instead of SQLite for reliability
- Or use a service like MongoDB Atlas for document storage

## Current Configuration Files Created

✅ **Procfile** - Tells Render how to run your app
✅ **runtime.txt** - Specifies Python 3.12.1
✅ **requirements.txt** - Updated with `gunicorn==21.2.0`

## Next Steps After Deployment

1. **Test**: Visit your Render URL and try:
   - Logging in as admin (admin/admin123)
   - Viewing orders dashboard
   - Checking all admin features

2. **Update Razorpay** (if using payments):
   - Go to your Render app settings
   - Add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
   - Update to live keys from Razorpay dashboard

3. **Custom Domain** (optional):
   - Go to Render Settings
   - Add custom domain in **Custom Domains** section
   - Update DNS records with your domain provider

## Monitoring Your App

In Render Dashboard:
- **Logs**: View application output in real-time
- **Metrics**: Monitor CPU, memory, network usage
- **Deploys**: See deployment history and status

---

**💡 Tip**: Set up GitHub auto-deploy! Any push to your `main` branch will automatically deploy new changes to Render.

Need help? Check Render docs: https://render.com/docs
