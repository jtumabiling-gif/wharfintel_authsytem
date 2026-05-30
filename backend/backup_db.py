"""
WharfIntel Database Backup and Google Drive Upload
This script backs up your PostgreSQL database and uploads it to Google Drive
"""

import os
import sys
import json
import webbrowser
from datetime import datetime
from pathlib import Path

# Install required packages
def install_packages():
    required = ["psycopg2-binary", "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"]
    for package in required:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            print(f"Installing {package}...")
            os.system(f"{sys.executable} -m pip install {package}")

install_packages()

import psycopg2
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class DatabaseBackupManager:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'wharfintel',
            'user': 'postgres',
            'password': 'postgres'  # Update if different
        }
        self.backup_dir = Path.home() / "Documents" / "wharfintel_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def backup_database_python(self):
        """Backup database using Python (no pg_dump needed)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"wharfintel_backup_{timestamp}.sql"
        
        try:
            print(f"📦 Connecting to database: {self.db_config['database']}")
            
            # Connect to database
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            print("📥 Exporting database schema and data...")
            
            # Get all tables
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            with open(backup_file, 'w') as f:
                # Write header
                f.write(f"-- WharfIntel Database Backup\n")
                f.write(f"-- Created: {datetime.now()}\n")
                f.write(f"-- Tables: {len(tables)}\n\n")
                
                # Backup each table
                for table in tables:
                    f.write(f"\n-- Table: {table}\n")
                    f.write(f"TRUNCATE TABLE {table};\n\n")
                    
                    # Get table data
                    cursor.execute(f"SELECT * FROM {table}")
                    columns = [desc[0] for desc in cursor.description]
                    
                    # Write insert statements
                    for row in cursor.fetchall():
                        values = ', '.join(
                            f"'{val}'" if isinstance(val, str) else 
                            'NULL' if val is None else 
                            str(val)
                            for val in row
                        )
                        f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({values});\n")
            
            cursor.close()
            conn.close()
            
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            print(f"✅ Backup created: {backup_file.name} ({size_mb:.2f} MB)")
            return backup_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def authenticate_gdrive(self):
        """Authenticate with Google Drive"""
        creds = None
        token_file = self.backup_dir / "token.pickle"
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                import pickle
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("\n🔐 Google Drive Authentication Required")
                print("Opening browser for authentication...")
                
                # For local testing, use OAuth2 flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                import pickle
                pickle.dump(creds, token)
        
        return creds
    
    def upload_to_gdrive(self, file_path, creds=None):
        """Upload file to Google Drive"""
        try:
            if not creds:
                print("⚠️  Skipping Google Drive upload (authentication not configured)")
                print("To enable automatic upload:")
                print("1. Create OAuth credentials at: https://console.cloud.google.com")
                print("2. Save as 'credentials.json' in backend folder")
                print("3. Run this script again")
                return False
            
            print(f"\n📤 Uploading to Google Drive...")
            service = build('drive', 'v3', credentials=creds)
            
            file_metadata = {'name': Path(file_path).name}
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()
            
            print(f"✅ Uploaded successfully!")
            print(f"📎 File ID: {file.get('id')}")
            print(f"🔗 View: {file.get('webViewLink')}")
            return True
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False

def main():
    print("🗄️  WharfIntel Database Backup Manager")
    print("="*60)
    
    manager = DatabaseBackupManager()
    
    # Create backup
    backup_file = manager.backup_database_python()
    
    if backup_file:
        print("\n" + "="*60)
        print("BACKUP COMPLETE!")
        print("="*60)
        print(f"📁 Location: {backup_file}")
        print(f"💾 Size: {backup_file.stat().st_size / (1024*1024):.2f} MB")
        
        # Try to upload
        try:
            creds = manager.authenticate_gdrive()
            manager.upload_to_gdrive(str(backup_file), creds)
        except Exception as e:
            print(f"\n⚠️  Automatic upload skipped: {e}")
            print("\n📤 MANUAL UPLOAD TO GOOGLE DRIVE:")
            print(f"1. Go to: https://drive.google.com")
            print(f"2. Click 'New' → 'File upload'")
            print(f"3. Select: {backup_file}")
    else:
        print("❌ Backup failed")

if __name__ == "__main__":
    main()
