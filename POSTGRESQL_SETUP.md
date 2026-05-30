# WharfIntel PostgreSQL Setup Guide

## Quick Start (5 Minutes)

### Step 1: Install PostgreSQL
1. Download: https://www.postgresql.org/download/windows/
2. Run installer (PostgreSQL 15+ recommended)
3. **Important**: Set password for `postgres` user (note it down!)
4. Port: `5432` (default - keep this)
5. Check "pgAdmin" to install the GUI tool

### Step 2: Create Database
Open PowerShell and run:

```powershell
psql -U postgres -c "CREATE DATABASE wharfintel;"
```

If prompted for password, enter the one you set during PostgreSQL installation.

### Step 3: Verify Installation
```powershell
psql -U postgres -d wharfintel -c "SELECT 1;"
```

Should output: `1` (Connection successful!)

### Step 4: Update .env File (if needed)
Check `backend/.env`:

```
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/wharfintel
```

Replace `PASSWORD` with your PostgreSQL password if different from "postgres".

### Step 5: Install Python Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### Step 6: Run Backend
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
[OK] ETA Model Loaded from Disk
[OK] Congestion Model Online.
```

If you see connection errors, check your `.env` file!

### Step 7: Run Frontend (New Terminal)
```powershell
cd frontend
npm run dev
```

### Step 8: Open Application
Go to: **http://localhost:5173**

---

## Troubleshooting

### Error: "Connection refused" (localhost:5432)

**Solution:**
```powershell
# Check if PostgreSQL service is running
Get-Service -Name PostgreSQL*

# Start PostgreSQL service
Start-Service PostgreSQL*

# Verify connection
psql -U postgres -d wharfintel
```

### Error: "Database does not exist"

**Solution:**
```powershell
# Create database
psql -U postgres -c "CREATE DATABASE wharfintel;"

# Verify
psql -U postgres -l
```

### Error: "Authentication failed for user postgres"

**Solution:**
Edit `backend/.env`:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/wharfintel
```

### Error: "psql command not found"

**Solution:**
PostgreSQL not installed or not in PATH. 
1. Install PostgreSQL from: https://www.postgresql.org/download/windows/
2. Or add PostgreSQL bin folder to PATH:
   - Find: `C:\Program Files\PostgreSQL\15\bin`
   - Add to Windows PATH environment variable

---



## How to Open & View Your Database

### Option 1: Using pgAdmin (GUI - Easiest)

1. Open **pgAdmin** (installed with PostgreSQL)
2. Click "Servers" on the left panel
3. Right-click "PostgreSQL 15" → "Connect Server"
4. Enter your password
5. Expand "Databases" → Select `wharfintel`
6. Expand "Schemas" → "public" → "Tables"
7. Right-click any table → "View/Edit Data" → "All Rows"

---

## Useful PostgreSQL Commands

### Connect to Database
```powershell
psql -U postgres -d wharfintel
```

### List All Databases
```powershell
psql -U postgres -l
```

### View All Tables
```powershell
psql -U postgres -d wharfintel -c "\dt"
```

### View Users Table
```powershell
psql -U postgres -d wharfintel -c "SELECT * FROM users;"
```

### Delete Database (Clean Start)
```powershell
psql -U postgres -c "DROP DATABASE wharfintel;"
psql -U postgres -c "CREATE DATABASE wharfintel;"
```

### Check Database Size
```powershell
psql -U postgres -d wharfintel -c "SELECT pg_size_pretty(pg_database_size('wharfintel'));"
```

### Exit psql
```
\q
```

---

## Backup Database

### Export Database
```powershell
pg_dump -U postgres -d wharfintel > wharfintel_backup.sql
```

### Import Database
```powershell
psql -U postgres -d wharfintel < wharfintel_backup.sql
```

---

## Security Notes

✅ Passwords hashed with bcrypt
✅ Unique salt per user
✅ Pepper applied during verification
✅ PostgreSQL connection uses standard authentication
✅ Database credentials in `.env` (never commit!)

---

**Last Updated**: May 30, 2026