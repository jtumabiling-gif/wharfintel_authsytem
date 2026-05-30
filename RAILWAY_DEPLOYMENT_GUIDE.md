# RAILWAY.APP DEPLOYMENT GUIDE - WHARFINTEL

**Complete Step-by-Step Guide to Host WharfIntel Successfully**

---

## TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Prepare Your Project](#prepare-your-project)
3. [Create Railway Account](#create-railway-account)
4. [Deploy Backend](#deploy-backend)
5. [Deploy Frontend](#deploy-frontend)
6. [Configure Environment Variables](#configure-environment-variables)
7. [Test Your Deployment](#test-your-deployment)
8. [Troubleshooting](#troubleshooting)

---

## PREREQUISITES

Before starting, ensure you have:

✅ **GitHub Account** - https://github.com (Free)
✅ **Railway Account** - https://railway.app (Free Tier)
✅ **Git Installed** - https://git-scm.com
✅ **Your WharfIntel Project** - Ready to push to GitHub
✅ **PostgreSQL Database** - Can use Railway's free PostgreSQL

**Verify installations:**
```powershell
git --version
node --version
python --version
```

---

## PREPARE YOUR PROJECT

### Step 1: Create GitHub Repository

**Go to GitHub:**
1. Visit https://github.com/new
2. Repository name: `wharfintel_auth_secure` (use your preferred name)
3. Description: "Secure Registration and Login System"
4. Set to Public (Railway needs to access it)
5. Click "Create repository"

### Step 2: Push Your Project to GitHub

**In your project directory:**
```powershell
# Initialize git if not done
git init

# Add all files
git add .

# Commit
git commit -m "WharfIntel: Secure Registration and Login System"

# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/wharfintel_auth_secure.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify on GitHub:**
- Visit: https://github.com/YOUR_USERNAME/wharfintel_auth_secure
- You should see all your project files

### Step 3: Create Required Files for Deployment

#### **A. Backend Dockerfile**

Create file: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **B. Backend requirements.txt**

**Location:** `backend/requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
bcrypt==4.1.1
pydantic==2.5.0
```

#### **C. Frontend Dockerfile**

Create file: `frontend/Dockerfile`

```dockerfile
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Build
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve
RUN npm install -g serve

# Copy build from builder
COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
```

#### **D. railway.toml (Root Directory)**

Create file: `railway.toml`

```toml
[build]
builder = "dockerfile"
dockerfile = "Dockerfile"

[deploy]
startCommand = ""
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 5
```

#### **E. .env.example (Backend)**

Create file: `backend/.env.example`

```
DATABASE_URL=postgresql://postgres:postgres@localhost/wharfintel
WHARF_PEPPER=CyberSec@WharfIntel2026!Pepper
ENVIRONMENT=production
```

### Step 4: Push Updated Files to GitHub

```powershell
git add .
git commit -m "Add deployment configurations (Dockerfile, requirements.txt)"
git push origin main
```

---

## CREATE RAILWAY ACCOUNT

### Step 1: Sign Up

1. Visit https://railway.app
2. Click "Login" → "Sign up with GitHub"
3. Authorize Railway to access your GitHub
4. Complete signup

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub"
3. Click "Configure GitHub App"
4. Select your GitHub account
5. Choose repository: `wharfintel_auth_secure`
6. Click "Install & Continue"

---

## DEPLOY BACKEND

### Step 1: Add PostgreSQL Database

1. In Railway dashboard, click "Create New Service"
2. Select "PostgreSQL"
3. Wait for provisioning (1-2 minutes)
4. Click the PostgreSQL service
5. Copy the connection string (DATABASE_URL)

**Example:**
```
postgresql://postgres:randompassword@containers.railway.app:5432/railway
```

### Step 2: Deploy Backend

1. Click "New Service" → "GitHub Repo"
2. Select your repository
3. Choose "backend" folder (if prompted)
4. Configure settings:
   - **Name:** wharfintel-backend
   - **Environment:** Production
   - **Root Directory:** backend

### Step 3: Configure Backend Variables

1. Go to backend service
2. Click "Variables"
3. Add the following:

```
DATABASE_URL=postgresql://postgres:PASSWORD@containers.railway.app:5432/railway
WHARF_PEPPER=CyberSec@WharfIntel2026!Pepper
ENVIRONMENT=production
```

**Get DATABASE_URL from PostgreSQL service:**
1. Click PostgreSQL service
2. Click "Variables"
3. Copy `DATABASE_URL`

### Step 4: Wait for Deployment

- Railway automatically starts building
- Monitor the "Deployments" tab
- Wait for green checkmark (successful)
- Note the backend URL from "Domains" section

**Example Backend URL:**
```
https://wharfintel-backend-production.up.railway.app
```

---

## DEPLOY FRONTEND

### Step 1: Update API URL

**Edit file:** `frontend/src/services/api.js` (or similar)

```javascript
// Use environment variable or Railway backend URL
const API_BASE = import.meta.env.VITE_API_URL || 'https://wharfintel-backend-production.up.railway.app';

export const loginUser = async (username, password) => {
  const response = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return response.json();
};
```

**Or update in AuthPage.jsx:**

```javascript
// Replace this line:
const response = await fetch(`http://127.0.0.1:8000/${path}`, {

// With this:
const API_URL = import.meta.env.VITE_API_URL || 'https://wharfintel-backend-production.up.railway.app';
const response = await fetch(`${API_URL}/${path}`, {
```

### Step 2: Create vite.config.js

**Location:** `frontend/vite.config.js`

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  },
  preview: {
    port: 3000
  }
})
```

### Step 3: Update package.json

**Location:** `frontend/package.json`

```json
{
  "name": "wharfintel-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "start": "npm run build && serve -s dist -l 3000"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "framer-motion": "^10.16.4",
    "leaflet": "^1.9.4",
    "react-leaflet": "^4.2.1",
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8"
  }
}
```

### Step 4: Deploy Frontend

1. Push updated files to GitHub:

```powershell
git add .
git commit -m "Configure frontend for Railway deployment"
git push origin main
```

2. In Railway dashboard, click "New Service"
3. Select "GitHub Repo"
4. Select your repository
5. Configure:
   - **Name:** wharfintel-frontend
   - **Root Directory:** frontend
   - **Build Command:** npm run build
   - **Start Command:** npm start

### Step 5: Add Frontend Variables

1. Go to frontend service
2. Click "Variables"
3. Add:

```
VITE_API_URL=https://wharfintel-backend-production.up.railway.app
NODE_ENV=production
```

### Step 6: Wait for Deployment

- Monitor "Deployments" tab
- Green checkmark = successful
- Note frontend URL from "Domains"

**Example Frontend URL:**
```
https://wharfintel-frontend-production.up.railway.app
```

---

## CONFIGURE ENVIRONMENT VARIABLES

### Backend Variables

**In Railway Backend Service:**

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://user:pass@host/db` | PostgreSQL connection |
| `WHARF_PEPPER` | `CyberSec@WharfIntel2026!Pepper` | Secret pepper |
| `ENVIRONMENT` | `production` | Deployment environment |
| `CORS_ORIGINS` | `https://wharfintel-frontend-production.up.railway.app` | Frontend URL |

### Frontend Variables

**In Railway Frontend Service:**

| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_API_URL` | `https://wharfintel-backend-production.up.railway.app` | Backend API URL |
| `NODE_ENV` | `production` | Node environment |

---

## TEST YOUR DEPLOYMENT

### Step 1: Access Frontend

1. Open frontend URL in browser
2. Should see WharfIntel landing page
3. Navigation and buttons should work

### Step 2: Test Registration

1. Click "Sign Up"
2. Enter username: `testuser`
3. Enter password: `Test@Password2026`
4. Confirm password
5. Click "Create Account"
6. Should see success message

### Step 3: Test Login

1. Click "Login"
2. Enter username: `testuser`
3. Enter password: `Test@Password2026`
4. Click "Sign In"
5. Should see "Successfully Sign In" popup
6. Click "Continue"

### Step 4: Check Backend API

Visit: `https://wharfintel-backend-production.up.railway.app/docs`

- Should see Swagger UI
- Test `/register` endpoint
- Test `/login` endpoint

### Step 5: Verify Database

1. In Railway PostgreSQL service
2. Click "Connect" → "PostgreSQL Client"
3. Run query:

```sql
SELECT id, username, hashed_password FROM users;
```

- Should see registered users with hashed passwords
- NO plain text passwords!

---

## TROUBLESHOOTING

### Issue 1: Deployment Failed

**Solution:**
1. Check "Deployment Logs"
2. Look for error messages
3. Common issues:
   - Missing `requirements.txt`
   - Missing `Dockerfile`
   - Typos in environment variables

### Issue 2: Database Connection Error

**Solution:**
1. Verify `DATABASE_URL` is correct
2. Make sure PostgreSQL service is running
3. Check if variables are properly set:

```powershell
# In Railway terminal
echo $DATABASE_URL
```

### Issue 3: Frontend Can't Connect to Backend

**Solution:**
1. Update `VITE_API_URL` in frontend variables
2. Ensure backend URL is correct
3. Check CORS settings in backend:

```python
# In backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://wharfintel-frontend-production.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 4: "Cannot find module" Error

**Solution:**
1. Ensure `package.json` is in root of `frontend`
2. Ensure `requirements.txt` is in root of `backend`
3. Check for typos in file names

### Issue 5: Port Already in Use

**Solution:**
1. Railway auto-selects ports
2. Make sure Dockerfile uses `0.0.0.0:8000` (backend)
3. Make sure Dockerfile uses `0.0.0.0:3000` (frontend)

---

## FINAL PUBLIC URLS

**After successful deployment:**

```
🌐 Frontend (Landing Page):
https://wharfintel-frontend-production.up.railway.app

🔌 Backend API:
https://wharfintel-backend-production.up.railway.app

📚 API Documentation:
https://wharfintel-backend-production.up.railway.app/docs
```

---

## USEFUL RAILWAY COMMANDS

### View Logs

```powershell
railway logs
```

### Connect to Database

```powershell
railway connect postgres
```

### View Variables

```powershell
railway variables
```

### Redeploy

```powershell
railway up
```

---

## SUBMISSION EVIDENCE

**For your project submission, include:**

✅ Screenshots of:
1. Frontend landing page (with URL in address bar)
2. Registration form
3. Login form
4. "Successfully Sign In" popup
5. Railway dashboard showing both services

✅ Working URLs:
1. Frontend URL
2. Backend URL
3. API Docs URL

✅ Database screenshot showing:
1. Users table
2. Hashed passwords (NOT plain text)
3. No pepper column

✅ Code quality:
1. Well-organized source files
2. Comprehensive comments
3. Proper indentation

---

## SUMMARY CHECKLIST

- ✅ GitHub repository created and pushed
- ✅ Backend Dockerfile created
- ✅ Frontend Dockerfile created
- ✅ requirements.txt configured
- ✅ package.json configured
- ✅ Railway account created
- ✅ PostgreSQL database created
- ✅ Backend deployed successfully
- ✅ Frontend deployed successfully
- ✅ Environment variables configured
- ✅ Registration tested
- ✅ Login tested
- ✅ API endpoints verified
- ✅ Database verified (hashed passwords only)
- ✅ Public URLs documented

---

**Status:** Ready for Submission ✅

**Deadline:** June 3, 2026

**Live URLs:** Provided above

---

*For additional Railway documentation: https://docs.railway.app*
