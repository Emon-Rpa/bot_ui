# Deploying to Render.com

Complete guide to deploy your Multi-Platform Message Viewer to Render.com for free.

## Prerequisites

1. **GitHub Account** - Create one at https://github.com if you don't have it
2. **Render Account** - Sign up at https://render.com (use GitHub to sign in)
3. **Git installed** on your computer

## Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
cd /home/emon/Documents/bot_ui

# Initialize git repository
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit - Multi-Platform Message Viewer"
```

### 1.2 Create .gitignore

A `.gitignore` file is already created to exclude unnecessary files.

### 1.3 Push to GitHub

```bash
# Create a new repository on GitHub (via web interface)
# Then connect it:

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render

### 2.1 Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already connected)
4. Select your repository

### 2.2 Configure Service

Fill in the following settings:

**Basic Settings:**
- **Name:** `message-viewer` (or your preferred name)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance Type:**
- Select **"Free"** tier

### 2.3 Environment Variables (Optional)

If you want to add any environment variables:
- Click **"Advanced"**
- Add environment variables if needed

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Wait 2-5 minutes for deployment to complete

### 2.5 Get Your URL

Once deployed, you'll get a URL like:
```
https://message-viewer-xxxx.onrender.com
```

## Step 3: Test Your Deployment

### 3.1 Open Your App

Visit your Render URL in a browser. You should see your message viewer!

### 3.2 Test API Endpoints

```bash
# Replace with your actual Render URL
RENDER_URL="https://message-viewer-xxxx.onrender.com"

# Test platforms endpoint
curl $RENDER_URL/api/platforms

# Test groups endpoint
curl "$RENDER_URL/api/groups?platform=messenger"

# Test adding data
curl -X POST "$RENDER_URL/api/messages?platform=whatsapp" \
  -H "Content-Type: application/json" \
  -d '{
    "Source_name": "Test Channel",
    "posts": [{"Post_text": "Hello from Render!"}]
  }'
```

## Step 4: Update Your App

Whenever you make changes:

```bash
# Make your changes
# Then commit and push

git add .
git commit -m "Description of changes"
git push origin main
```

Render will **automatically redeploy** your app! 🚀

## Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- First request after spin-down takes 30-60 seconds (cold start)
- 750 hours/month (enough for one always-on service)
- Shared CPU and 512MB RAM

### Data Persistence

⚠️ **Important:** Free tier uses **ephemeral storage**
- Data in JSON files will be **lost on restart**
- Each deployment creates a fresh instance

**Solutions:**
1. **Use a database** (PostgreSQL - Render offers free tier)
2. **Use external storage** (AWS S3, Cloudinary)
3. **Accept data loss** (for testing/demo purposes)

### Keeping Your App Awake

Free tier apps sleep after 15 minutes. To keep it awake:

**Option 1: Use a ping service**
- https://uptimerobot.com (free)
- Ping your app every 10 minutes

**Option 2: Upgrade to paid tier** ($7/month)
- No sleep
- Persistent storage
- Better performance

## Step 5: Using Your Deployed App

### Update API Calls

In your scripts or Postman, replace `localhost:5000` with your Render URL:

**Before:**
```
http://localhost:5000/api/messages
```

**After:**
```
https://message-viewer-xxxx.onrender.com/api/messages
```

### Share Your App

Your app is now publicly accessible! Share the URL with anyone:
```
https://message-viewer-xxxx.onrender.com
```

## Troubleshooting

### Deployment Failed

**Check Logs:**
1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. Look for error messages

**Common Issues:**
- **Missing dependencies:** Check `requirements.txt`
- **Port issues:** Render automatically sets PORT environment variable
- **Python version:** Check `runtime.txt`

### App Not Loading

1. **Check deployment status** in Render dashboard
2. **View logs** for errors
3. **Verify build completed** successfully
4. **Check if app is sleeping** (free tier)

### Data Not Persisting

This is expected on free tier. Solutions:
1. Add PostgreSQL database (free tier available)
2. Use external storage service
3. Upgrade to paid tier with persistent disk

## Upgrading to Paid Tier

If you need:
- ✅ No sleep/downtime
- ✅ Persistent storage
- ✅ Better performance
- ✅ Custom domain

Upgrade to **Starter** tier ($7/month):
1. Go to service settings
2. Change instance type to "Starter"
3. Add persistent disk if needed

## Alternative: Add PostgreSQL Database

To persist data across deployments:

### 1. Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Name it `message-viewer-db`
3. Select **Free** tier
4. Click **"Create Database"**

### 2. Update Your App

You'll need to modify `app.py` to use PostgreSQL instead of JSON files.
This requires additional code changes (let me know if you want help with this).

## Summary

✅ **What You've Done:**
- Created deployment configuration files
- Prepared app for Render.com
- Learned how to deploy and update

✅ **Next Steps:**
1. Push code to GitHub
2. Create Render web service
3. Deploy and test
4. Share your live app!

✅ **Your App Will Be Live At:**
```
https://YOUR-APP-NAME.onrender.com
```

Need help with any step? Let me know! 🚀
