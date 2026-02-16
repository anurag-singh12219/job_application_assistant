# Deployment Guide - AI Job Application Assistant

Complete guide to deploy your application online for free.

## Recommended Stack (Free Tier)

- **Backend**: Render.com (Free)
- **Frontend**: Vercel.com (Free)
- **Total Cost**: $0/month

---

## Option 1: Deploy on Render + Vercel (Recommended)

### Part A: Deploy Backend on Render

**Step 1: Create Render Account**
1. Go to https://render.com
2. Sign up with GitHub (use your anurag-singh12219 account)
3. Authorize Render to access your repositories

**Step 2: Create Web Service**
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `job_application_assistant`
3. Configure:
   - **Name**: `job-assistant-api`
   - **Region**: Choose closest to you
   - **Branch**: `master`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

**Step 3: Add Environment Variables**

In Render dashboard, add:
```
GROQ_API_KEY=your_groq_api_key
ADZUNA_APP_ID=your_adzuna_id
ADZUNA_APP_KEY=your_adzuna_key
PYTHONUNBUFFERED=1
```

**Step 4: Deploy**
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Your backend will be at: `https://job-assistant-api.onrender.com`

**Step 5: Test Backend**
```bash
curl https://job-assistant-api.onrender.com/health
# Should return: {"status":"healthy","service":"AI Job Application Assistant"}
```

---

### Part B: Deploy Frontend on Vercel

**Step 1: Update Backend URL**

Edit `ai-frontend/src/api/backend.js`:
```javascript
// Change this line
const API_URL = process.env.VITE_API_URL || "https://job-assistant-api.onrender.com";
```

Commit and push:
```bash
git add ai-frontend/src/api/backend.js
git commit -m "feat: add production backend URL"
git push origin master
```

**Step 2: Create Vercel Account**
1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel

**Step 3: Import Project**
1. Click **"Add New..."** → **"Project"**
2. Import `job_application_assistant` repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `ai-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

**Step 4: Add Environment Variable**
- Key: `VITE_API_URL`
- Value: `https://job-assistant-api.onrender.com`

**Step 5: Deploy**
- Click **"Deploy"**
- Wait 2-3 minutes
- Your frontend will be at: `https://job-application-assistant.vercel.app`

**Step 6: Access Your App**
Open: `https://job-application-assistant.vercel.app`

---

## Option 2: Deploy Everything on Render

**Deploy Backend** (same as above)

**Deploy Frontend as Static Site:**

1. Build frontend locally:
```bash
cd ai-frontend
npm run build
```

2. Create new **Static Site** on Render:
   - Branch: `master`
   - Root Directory: `ai-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

---

## Option 3: Deploy on Railway (Alternative)

**Step 1: Create Railway Account**
1. Go to https://railway.app
2. Sign up with GitHub

**Step 2: Deploy Backend**
1. Click **"New Project"** → **"Deploy from GitHub repo"**
2. Select `job_application_assistant`
3. Railway auto-detects Python
4. Add environment variables in dashboard
5. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 3: Deploy Frontend**
1. Same project, click **"New Service"**
2. Select same repo
3. Railway detects Node.js
4. Builds and deploys automatically

---

## Custom Domain (Optional)

### For Vercel Frontend:
1. Go to Vercel dashboard → Your project
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain (e.g., `job-assistant.com`)
4. Update DNS records as shown

### For Render Backend:
1. Go to Render dashboard → Your service
2. Click **"Settings"** → **"Custom Domain"**
3. Add API subdomain (e.g., `api.job-assistant.com`)

---

## CORS Configuration

Make sure your backend allows frontend domain. In `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://job-application-assistant.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Monitoring & Maintenance

### Render Free Tier Limitations:
- Service spins down after 15 minutes of inactivity
- First request after inactivity takes ~30 seconds
- 750 hours/month free (enough for one service 24/7)

### Keep Backend Alive:
Use a free service like UptimeRobot:
1. Go to https://uptimerobot.com
2. Add monitor for your API: `https://job-assistant-api.onrender.com/health`
3. Check every 5 minutes
4. Keeps your service warm

### Vercel Free Tier:
- Unlimited deployments
- 100 GB bandwidth/month
- Automatic HTTPS
- No sleeping/spindown

---

## Troubleshooting

**Backend not starting on Render:**
- Check logs in Render dashboard
- Verify all dependencies in requirements.txt
- Ensure spaCy model downloads in build command

**Frontend can't connect to backend:**
- Check CORS settings in main.py
- Verify API_URL in frontend code
- Check browser console for errors

**Slow first load:**
- Normal for Render free tier (cold start)
- Consider using UptimeRobot to keep warm

**Environment variables not working:**
- Redeploy after adding variables
- Check variable names match code

---

## Deployment Checklist

**Before deploying:**
- [ ] Push all code to GitHub
- [ ] Get API keys (Groq, Adzuna)
- [ ] Test locally (backend + frontend)
- [ ] Update CORS settings
- [ ] Update frontend API URL

**Backend deployment:**
- [ ] Render account created
- [ ] Web service configured
- [ ] Environment variables added
- [ ] Build successful
- [ ] /health endpoint responds

**Frontend deployment:**
- [ ] Vercel account created
- [ ] Project imported
- [ ] Build successful
- [ ] Can access deployed site
- [ ] Backend connection works

**Post-deployment:**
- [ ] Test all features online
- [ ] Set up monitoring (UptimeRobot)
- [ ] Add custom domain (optional)
- [ ] Share deployed URL on LinkedIn/GitHub

---

## Deployed URLs

After deployment, update your README.md with:

```markdown
## 🌐 Live Demo

**Frontend**: https://job-application-assistant.vercel.app
**API**: https://job-assistant-api.onrender.com
**API Docs**: https://job-assistant-api.onrender.com/docs
```

---

## Cost Breakdown

| Service | Free Tier | Limitations |
|---------|-----------|-------------|
| Render | 750 hrs/month | Spins down after 15 min idle |
| Vercel | Unlimited | 100 GB bandwidth/month |
| **Total** | **$0/month** | Sufficient for portfolio project |

---

## Upgrading (Optional)

**If you need always-on backend:**
- Render Starter: $7/month
- Railway Hobby: $5/month
- Heroku Basic: $7/month

**For your portfolio project, free tier is sufficient!**

---

## Next Steps

1. Deploy backend on Render (15 minutes)
2. Deploy frontend on Vercel (5 minutes)
3. Test deployed application (5 minutes)
4. Update README with live URLs
5. Share on LinkedIn with live demo link!

---

## Support

Issues during deployment?
1. Check service logs in dashboard
2. Read troubleshooting section above
3. Open issue on GitHub
4. Check Render/Vercel documentation

**Render Docs**: https://render.com/docs
**Vercel Docs**: https://vercel.com/docs

---

**Ready to deploy? Follow Option 1 (Render + Vercel) for best results!** 🚀
