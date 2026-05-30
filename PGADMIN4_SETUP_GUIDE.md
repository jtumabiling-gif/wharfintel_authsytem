# pgAdmin4 Database Setup & Restore Guide

## Part 1: Access pgAdmin4

### Step 1: Open pgAdmin4
1. Open your browser and go to: **http://localhost:5050** (or your pgAdmin4 URL)
2. Login with your credentials (default: admin@pgadmin.org / admin)

### Step 2: Connect to PostgreSQL Server
1. In the left sidebar, expand **"Servers"**
2. Right-click on your PostgreSQL server (usually "PostgreSQL 15" or similar)
3. Click **"Connect Server"** if not already connected
4. Enter your PostgreSQL password if prompted

---

## Part 2: Restore Backup Using pgAdmin4

### Method 1: Using SQL File (Recommended for .sql files)

1. **Navigate to Database**
   - In left sidebar: Servers → PostgreSQL → Databases
   - Right-click on **"wharfintel"** database
   - Select **"Query Tool"**

2. **Load and Run SQL File**
   - Click the folder icon or press **Ctrl+O**
   - Select: `C:\Users\Administrator\Documents\wharfintel_backups\wharfintel_backup_20260530_170044.sql`
   - Click **"Execute"** or press **F5**
   - Wait for completion (you'll see "Query completed successfully")

3. **Verify Data**
   - Expand: Databases → wharfintel → Schemas → public → Tables
   - Right-click **"users"** → Select **"View/Edit Data"** → All Rows
   - You should see the 3 users (Jwt, Gab, Janwen)

### Method 2: Using Restore Function (More robust)

1. **Create Empty Database** (if needed)
   - Right-click on **"Databases"** in left sidebar
   - Select **"Create"** → **"Database"**
   - Name: `wharfintel`
   - Click **"Save"**

2. **Restore Backup**
   - Right-click on **"wharfintel"** database
   - Select **"Restore"**
   - In the dialog:
     - **Filename**: Browse to your backup file
     - **Format**: Select based on file type:
       - `.sql` file → "Plain"
       - `.dump` or `.backup` file → "Custom"
   - Click **"Restore"**

3. **Monitor Progress**
   - A popup will show: "Restore (Process created PID xxxx)"
   - Wait until you see: "Process exited with code 0"

---

## Part 3: Backup Database Using pgAdmin4

### Method 1: Export as SQL (Human-readable)

1. **Right-click Database**
   - Right-click **"wharfintel"** in left sidebar
   - Select **"Backup..."**

2. **Configure Backup**
   - **General Tab**:
     - Filename: `wharfintel_backup_YYYYMMDD.sql`
     - Format: **Plain** ✓
     - Encoding: UTF8
   - **Dump Options Tab**:
     - ✓ Include CREATE DATABASE statement
     - ✓ Data
     - ✓ Schema
   - Click **"Backup"**

3. **Save Location**
   - Choose: `C:\Users\Administrator\Documents\wharfintel_backups\`
   - File will be created automatically

### Method 2: Export as Custom Format (Compressed, smaller file)

1. **Right-click Database** → **"Backup..."**
2. **Configure Backup**
   - Filename: `wharfintel_backup_YYYYMMDD.dump`
   - Format: **Custom** ✓
   - Compression: `gzip` (recommended)
   - Click **"Backup"**

---

## Part 4: Upload Backup to Google Drive

### Using Browser:
1. Go to **https://drive.google.com**
2. Click **"New"** → **"File upload"**
3. Select your backup file from `C:\Users\Administrator\Documents\wharfintel_backups\`
4. Wait for upload to complete

### Using Python Script (Automated):
```bash
cd "c:\Users\Administrator\Documents\flutter projects dev\WharfIntel-main\backend"
python backup_db.py
```

---

## Part 5: Common pgAdmin4 Tasks

### View Database Tables
1. Left sidebar: Servers → PostgreSQL → Databases → wharfintel → Schemas → public → Tables
2. Right-click any table → **"View/Edit Data"**
3. Select **"All Rows"** to see data

### Run SQL Queries
1. Right-click **"wharfintel"** database
2. Click **"Query Tool"**
3. Write your SQL:
   ```sql
   SELECT * FROM users;
   SELECT * FROM shipments;
   ```
4. Press **F5** or click Execute button

### Check Table Structure
1. Right-click table name → **"Properties"**
2. View columns, data types, constraints

### Delete & Recreate Database
1. Right-click **"wharfintel"** → **"Delete/Drop"**
2. Confirm deletion
3. Right-click **"Databases"** → **"Create"** → **"Database"**
4. Restore from backup (see Part 3, Method 2)

---

## Troubleshooting

### Issue: "Permission denied" when accessing pgAdmin4
- **Solution**: pgAdmin4 may not be running
- Start pgAdmin4 service or run: `pgadmin4` in terminal

### Issue: Cannot connect to PostgreSQL server
- **Solution**: 
  - Make sure PostgreSQL is running
  - Check server connection: Right-click server → "Connect Server"
  - Verify credentials in connection properties

### Issue: Backup file is very small (0 KB)
- **Solution**:
  - Database may be empty
  - Try using the SQL query method to verify data exists:
    ```sql
    SELECT COUNT(*) FROM users;
    SELECT COUNT(*) FROM shipments;
    ```

### Issue: Restore fails with errors
- **Solution**:
  - Try dropping and recreating the database first
  - Use "Query Tool" to manually run the SQL file
  - Check for encoding issues (UTF-8)

---

## Quick Reference: File Locations

| Item | Location |
|------|----------|
| Backup files | `C:\Users\Administrator\Documents\wharfintel_backups\` |
| Latest backup | `wharfintel_backup_20260530_170044.sql` |
| Python backup script | `backend/backup_db.py` |
| PostgreSQL bin | `C:\Program Files\PostgreSQL\15\bin\` |
| pgAdmin4 | http://localhost:5050 |

---
