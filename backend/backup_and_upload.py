import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Install required packages
def install_packages():
    try:
        import google
    except ImportError:
        print("Installing google-auth-oauthlib and google-auth-httplib2...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "google-auth-oauthlib", "google-auth-httplib2", "google-api-python-client"])

install_packages()

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_drive_api import GoogleDriveUploader
import pickle

class DatabaseBackupManager:
    def __init__(self):
        self.db_user = "postgres"
        self.db_name = "wharfintel"
        self.db_host = "localhost"
        self.backup_dir = Path.home() / "Documents" / "wharfintel_backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def backup_database_sql(self):
        """Backup database as SQL file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"wharfintel_backup_{timestamp}.sql"
        
        try:
            print(f"📦 Creating SQL backup: {backup_file.name}")
            # Note: This command requires password input or .pgpass file
            cmd = f'pg_dump -U {self.db_user} -d {self.db_name} -h {self.db_host} > "{backup_file}"'
            result = os.system(cmd)
            
            if result == 0 and backup_file.exists():
                size_mb = backup_file.stat().st_size / (1024 * 1024)
                print(f"✅ Backup created successfully: {size_mb:.2f} MB")
                return backup_file
            else:
                print("❌ Backup failed. Make sure PostgreSQL bin is in PATH")
                return None
        except Exception as e:
            print(f"❌ Error during backup: {e}")
            return None
    
    def backup_database_dump(self):
        """Backup database as compressed dump file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"wharfintel_backup_{timestamp}.dump"
        
        try:
            print(f"📦 Creating compressed dump: {backup_file.name}")
            cmd = f'pg_dump -U {self.db_user} -d {self.db_name} -h {self.db_host} -F c -f "{backup_file}"'
            result = os.system(cmd)
            
            if result == 0 and backup_file.exists():
                size_mb = backup_file.stat().st_size / (1024 * 1024)
                print(f"✅ Dump created successfully: {size_mb:.2f} MB")
                return backup_file
            else:
                print("❌ Dump failed. Make sure PostgreSQL bin is in PATH")
                return None
        except Exception as e:
            print(f"❌ Error during dump: {e}")
            return None

def upload_to_gdrive(file_path):
    """Upload file to Google Drive"""
    print(f"\n📤 Uploading to Google Drive...")
    print(f"File: {file_path}")
    
    # For manual upload guide
    print("\n" + "="*60)
    print("MANUAL UPLOAD TO GOOGLE DRIVE:")
    print("="*60)
    print(f"1. Open: https://drive.google.com")
    print(f"2. Click 'New' → 'File upload'")
    print(f"3. Select: {file_path}")
    print(f"4. Done!")
    print("="*60 + "\n")

if __name__ == "__main__":
    manager = DatabaseBackupManager()
    
    print("🗄️  WharfIntel Database Backup Manager")
    print("="*50)
    
    # Create backup
    backup_file = manager.backup_database_sql()
    
    if backup_file:
        upload_to_gdrive(str(backup_file))
        print(f"✅ Backup file ready at: {backup_file}")
    else:
        print("❌ Failed to create backup")
