# FREE WEB HOSTING ALTERNATIVES TO RAILWAY

**Complete Guide to Deploy WharfIntel Using Different Free Services**

---

## COMPARISON TABLE

| Service | Backend | Frontend | Database | Free Tier | Ease |
|---------|---------|----------|----------|-----------|------|
| **Railway** | ✅ | ✅ | ✅ | $5/month credit | ⭐⭐⭐ |
| **Render** | ✅ | ✅ | ✅ | Limited (sleeps) | ⭐⭐⭐ |
| **Heroku** | ✅ | ✅ | ✅ | Paid only (Oct 2022) | ❌ |
| **Vercel** | ❌ | ✅ | ❌ | Generous | ⭐⭐⭐⭐ |
| **Netlify** | ❌ | ✅ | ❌ | Generous | ⭐⭐⭐⭐ |
| **Replit** | ✅ | ✅ | ✅ | Limited | ⭐⭐⭐ |
| **PythonAnywhere** | ✅ | ❌ | ✅ | Limited | ⭐⭐⭐ |
| **AWS** | ✅ | ✅ | ✅ | 12 months free | ⭐⭐ |
| **Google Cloud** | ✅ | ✅ | ✅ | $300 credit | ⭐⭐ |
| **Azure** | ✅ | ✅ | ✅ | $200 credit | ⭐⭐ |

---

## OPTION 1: RENDER (Recommended - Best Free Alternative)

**Pros:** Similar to Railway, good free tier, easy deployment, free PostgreSQL
**Cons:** Services go to sleep after 15 min inactivity on free tier

### Step-by-Step Deployment

#### **A. Create Render Account**
1. Visit: https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize access

#### **B. Deploy Backend**

1. **Create Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect GitHub repository
   - Select `wharfintel_auth_secure` repository

2. **Configure Backend**
   - Name: `wharfintel-backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Root Directory: `backend`

3. **Add Environment Variables**
   - `DATABASE_URL`: Will get from PostgreSQL step
   - `WHARF_PEPPER`: `CyberSec@WharfIntel2026!Pepper`
   - `ENVIRONMENT`: `production`

4. **Create PostgreSQL**
   - Dashboard → "New +" → "PostgreSQL"
   - Name: `wharfintel-db`
   - Database: `wharfintel`
   - Region: Same as backend
   - Copy the `Internal Database URL`

5. **Update Backend Variables**
   - Copy PostgreSQL "Internal Database URL"
   - In backend service → "Environment" → Edit `DATABASE_URL`
   - Paste the URL

#### **C. Deploy Frontend**

1. **Create Static Site Service**
   - Dashboard → "New +" → "Static Site"
   - Connect GitHub repository

2. **Configure Frontend**
   - Name: `wharfintel-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Root Directory: `frontend`

3. **Add Frontend Variables**
   - `VITE_API_URL`: Backend service URL (from Render dashboard)
   - `NODE_ENV`: `production`

#### **IMPORTANT: If you get "vite: not found" error:**

The issue is that Vite needs to be installed. Fix it:

1. **Update frontend/package.json:**
   - Move `vite` and `@vitejs/plugin-react` from `devDependencies` to `dependencies`
   - Update build script to: `npm install && npm run build`

2. **Or use Dockerfile instead:**
   - Render also accepts Dockerfiles
   - Create `frontend/Dockerfile` (multi-stage build)
   - In Render, select "Docker" runtime instead of "Static Site"

3. **Or use Custom Build Command:**
   - Build Command: `npm ci && npm run build`
   - Start Command: `npx serve -s dist -l 3000`

#### **D. Get Public URLs**
- Backend URL: Shown in backend service page
- Frontend URL: Shown in frontend service page

**Example:**
```
Frontend: https://wharfintel-frontend.onrender.com
Backend: https://wharfintel-backend.onrender.com
```

---

## OPTION 2: VERCEL (Best for Frontend Only)

**Pros:** Excellent free tier, fast, great for React/Vue
**Cons:** Backend not supported (must use external API)

### Deploy Frontend to Vercel

#### **Step 1: Create Account**
1. Visit: https://vercel.com
2. "Sign Up" → "Continue with GitHub"
3. Authorize Vercel

#### **Step 2: Deploy Frontend**
1. Dashboard → "Add New..." → "Project"
2. Select your GitHub repository
3. Choose "frontend" folder

#### **Step 3: Configure**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

#### **Step 4: Environment Variables**
- `VITE_API_URL`: Your Railway/Render backend URL

#### **Step 5: Deploy**
- Click "Deploy"
- Wait for build to complete
- Get public URL

**Example:**
```
https://wharfintel-frontend.vercel.app
```

---

## OPTION 3: NETLIFY (Alternative for Frontend)

**Pros:** Easy deployment, good free tier, good support
**Cons:** Same as Vercel - frontend only

### Deploy Frontend to Netlify

#### **Step 1: Create Account**
1. Visit: https://netlify.com
2. "Sign up" → "GitHub"
3. Authorize Netlify

#### **Step 2: Deploy**
1. "Sites" → "Add new site" → "Import an existing project"
2. Choose GitHub
3. Select your repository
4. Choose `frontend` folder

#### **Step 3: Configure Build**
- Build command: `npm run build`
- Publish directory: `dist`

#### **Step 4: Environment Variables**
- Go to Site settings → Build & Deploy → Environment
- Add: `VITE_API_URL=https://your-backend-url.com`

#### **Step 5: Done!**
- Netlify automatically deploys on git push
- Get public URL from Site overview

**Example:**
```
https://wharfintel-frontend.netlify.app
```

---

## OPTION 4: REPLIT (All-in-One Solution)

**Pros:** Everything in one place, easy for beginners
**Cons:** Limited free tier, can be slow

### Deploy Full Stack to Replit

#### **Step 1: Create Account**
1. Visit: https://replit.com
2. "Sign up" → "GitHub"
3. Authorize Replit

#### **Step 2: Import Repository**
1. "+ Create" → "Import from GitHub"
2. Paste: `https://github.com/YOUR_USERNAME/wharfintel_auth_secure`
3. Click "Import"

#### **Step 3: Create .replit File**
- Create file: `.replit`
- Add:
```toml
run = "bash start.sh"
```

#### **Step 4: Create start.sh**
```bash
#!/bin/bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
cd ../frontend
npm install
npm run build
npm start
```

#### **Step 5: Set Secrets**
- In Replit, go to "Secrets" (lock icon)
- Add:
  - `DATABASE_URL`: `postgresql://...`
  - `WHARF_PEPPER`: `CyberSec@WharfIntel2026!Pepper`

#### **Step 6: Run**
- Click "Run" button
- Replit shows public URL

**Example:**
```
https://wharfintel-auth-secure.replit.dev
```

---

## OPTION 5: PYTHON ANYWHERE (Backend Only)

**Pros:** Perfect for Python/FastAPI, free tier available
**Cons:** Limited free tier, frontend needs separate hosting

### Deploy Backend to PythonAnywhere

#### **Step 1: Create Account**
1. Visit: https://pythonanywhere.com
2. "Create a new free account"
3. Verify email

#### **Step 2: Upload Code**
1. Go to Files → Upload a zip
2. Or use Git (Web → "Add a new web app")

#### **Step 3: Configure Web App**
1. Web → "Add a new web app"
2. Python 3.11
3. Select "FastAPI"
4. Configure path to `app.main:app`

#### **Step 4: Set Environment Variables**
1. Web → Edit WSGI file
2. Add:
```python
import os
os.environ['DATABASE_URL'] = 'postgresql://...'
os.environ['WHARF_PEPPER'] = 'CyberSec@WharfIntel2026!Pepper'
```

#### **Step 5: Add PostgreSQL**
1. Databases → Add MySQL/PostgreSQL
2. PythonAnywhere provides free database

#### **Step 6: Reload Web App**
- Click "Reload" button
- Get public URL: `https://yourusername.pythonanywhere.com`

---

## OPTION 6: AWS (Free Tier 12 Months)

**Pros:** Most powerful, 12-month free tier
**Cons:** Complex, steep learning curve

### Quick AWS Deployment

#### **Services to Use:**
- **Backend:** AWS Elastic Beanstalk or EC2
- **Frontend:** AWS Amplify
- **Database:** AWS RDS (PostgreSQL)

#### **Basic Steps:**
1. Create AWS account: https://aws.amazon.com/free
2. Create Elastic Beanstalk environment
3. Deploy via Git or ZIP upload
4. Configure RDS PostgreSQL database
5. Set environment variables in Beanstalk
6. Deploy frontend with AWS Amplify

**More info:** https://docs.aws.amazon.com/elasticbeanstalk/

---

## OPTION 7: GOOGLE CLOUD (Free $300 Credit)

**Pros:** Powerful, good for learning
**Cons:** Complex setup, can be expensive after credit runs out

### Quick Google Cloud Deployment

#### **Services:**
- **Backend:** Cloud Run
- **Frontend:** Firebase Hosting
- **Database:** Cloud SQL (PostgreSQL)

#### **Steps:**
1. Create account: https://cloud.google.com/free
2. Create Cloud Run service
3. Push Docker image to Container Registry
4. Deploy to Cloud Run
5. Create Cloud SQL PostgreSQL instance
6. Deploy frontend to Firebase Hosting

**More info:** https://cloud.google.com/run/docs

---

## OPTION 8: AZURE (Free $200 Credit)

**Pros:** Enterprise-grade, good support
**Cons:** Complex, credit expires after 30 days

### Quick Azure Deployment

#### **Services:**
- **Backend:** Azure App Service
- **Frontend:** Azure Static Web Apps
- **Database:** Azure Database for PostgreSQL

#### **Steps:**
1. Create account: https://azure.microsoft.com/free
2. Create App Service
3. Deploy via GitHub Actions
4. Create Azure Database for PostgreSQL
5. Deploy frontend to Static Web Apps

**More info:** https://azure.microsoft.com/services/app-service/

---

## RECOMMENDED COMBINATIONS

### Option A: Best Free Setup (Recommended)
```
✅ Backend: Render (with free PostgreSQL)
✅ Frontend: Vercel or Netlify
✅ Database: Render PostgreSQL
✅ Cost: FREE forever
```

### Option B: Best All-in-One
```
✅ Everything: Railway
✅ Cost: FREE tier with generous limits
```

### Option C: Best for Learning
```
✅ Backend: PythonAnywhere
✅ Frontend: Vercel
✅ Database: PythonAnywhere
✅ Cost: FREE with limitations
```

### Option D: Enterprise (Time-Limited Free)
```
✅ Everything: AWS/Google Cloud/Azure
✅ Cost: FREE for 12 months / $300 credit
```

---

## STEP-BY-STEP: RENDER + VERCEL (RECOMMENDED)

### A. Deploy Backend to Render

1. Visit: https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your GitHub repo
5. Configure:
   - Name: `wharfintel-backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Root Directory: `backend`
6. Click "Create Web Service"

### B. Create PostgreSQL on Render

1. Dashboard → "New +" → "PostgreSQL"
2. Name: `wharfintel-db`
3. Region: Same as backend
4. Click "Create Database"
5. Copy "Internal Database URL"

### C. Update Backend Variables

1. Go to backend service
2. Click "Environment"
3. Add:
   - `DATABASE_URL`: Paste PostgreSQL URL
   - `WHARF_PEPPER`: `CyberSec@WharfIntel2026!Pepper`
4. Click "Save"
5. Service auto-redeploys

### D. Get Backend URL

- Backend service page shows: `https://wharfintel-backend.onrender.com`

### E. Deploy Frontend to Vercel

1. Visit: https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Select your GitHub repo
5. Configure:
   - Framework: React
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Root Directory: `frontend`
6. Click "Deploy"

### F. Add Frontend Variables in Vercel

1. Project Settings → "Environment Variables"
2. Add:
   - `VITE_API_URL`: `https://wharfintel-backend.onrender.com`
3. Click "Save"
4. Click "Redeploy"

### G. Get Frontend URL

- Project page shows: `https://wharfintel-frontend.vercel.app`

### H. Update Your Code

**In `frontend/src/pages/AuthPage.jsx`:**
```javascript
// Replace this:
// const API_URL = 'http://127.0.0.1:8000';

// With this:
const API_URL = import.meta.env.VITE_API_URL || 'https://wharfintel-backend.onrender.com';
```

### I. Push Changes to GitHub

```powershell
git add .
git commit -m "Update API URL for production deployment"
git push origin main
```

### J. Both Services Auto-Deploy

- Vercel auto-redeploys after push
- Frontend now connects to Render backend
- Done! ✅

---

## FINAL PUBLIC URLS

```
🌐 Frontend (Vercel):
https://wharfintel-frontend.vercel.app

🔌 Backend API (Render):
https://wharfintel-backend.onrender.com

📚 API Docs:
https://wharfintel-backend.onrender.com/docs
```

---

## SUMMARY

| Need | Best Service | Free | Difficulty |
|------|--------------|------|-----------|
| Full Stack | Render | ✅ Yes | Easy |
| Frontend Only | Vercel | ✅ Yes | Very Easy |
| Python Backend | Render | ✅ Yes | Easy |
| Enterprise Ready | AWS/GCP/Azure | 🕐 12 months | Hard |
| Simplest Setup | Replit | ✅ Limited | Very Easy |

---

## WHICH ONE TO CHOOSE?

**I recommend: RENDER + VERCEL**

Why?
- ✅ Completely FREE forever
- ✅ Easy to use (similar to Railway)
- ✅ Good uptime and performance
- ✅ Render gives free PostgreSQL
- ✅ Vercel is incredibly fast for frontend
- ✅ Combined solution is very reliable

**Second choice: Railway**
- Great free tier with $5 credit
- All-in-one solution
- Easy deployment

---

*Choose based on your needs and comfort level!*
