# Quick Deployment Checklist - Render

## ✅ Files Already Prepared
- `Procfile` ✓ - Ready to run on Render
- `runtime.txt` ✓ - Python 3.12.1
- `requirements.txt` ✓ - Updated with gunicorn
- `DEPLOYMENT.md` ✓ - Full deployment guide

## 🚀 Quick Steps (5 minutes)

### 1. Push to GitHub
```powershell
cd d:\VS code\canteen
git init
git add .
git commit -m "College Canteen - Ready for deployment"
git remote add origin https://github.com/USERNAME/college-canteen.git
git branch -M main
git push -u origin main
```
*(Replace USERNAME with your GitHub username)*

### 2. Deploy on Render
1. Go to **render.com** → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Fill in:
   - **Name**: college-canteen
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
5. Click **"Create Web Service"**
6. Wait 5-10 minutes for deployment

### 3. Access Your App
Once deployed, Render gives you a URL:
```
https://college-canteen-xxxx.onrender.com
```

**Login**: 
- Username: `admin`
- Password: `admin123`

---

## 📝 Important Notes

⚠️ **Database**: Currently using SQLite. For better reliability with multiple users, upgrade to PostgreSQL (see full DEPLOYMENT.md)

⚠️ **Razorpay**: Add your credentials in Render environment variables

⚠️ **SECRET_KEY**: Add a random string in Render environment variables

---

**For detailed instructions, see: DEPLOYMENT.md** 📖
