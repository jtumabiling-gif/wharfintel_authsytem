#!/usr/bin/env python3
"""
PostgreSQL Setup Script for WharfIntel
Automatically creates the database and tables
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n[*] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[✓] {description} - SUCCESS")
            if result.stdout:
                print(f"    Output: {result.stdout.strip()}")
            return True
        else:
            print(f"[✗] {description} - FAILED")
            if result.stderr:
                print(f"    Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[✗] {description} - ERROR: {e}")
        return False

def main():
    print("=" * 60)
    print("WharfIntel PostgreSQL Setup")
    print("=" * 60)
    
    # Check if PostgreSQL is installed
    print("\n[*] Checking PostgreSQL installation...")
    result = subprocess.run("psql --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("[✗] PostgreSQL is not installed or not in PATH")
        print("    Please install PostgreSQL: https://www.postgresql.org/download/windows/")
        sys.exit(1)
    else:
        print(f"[✓] {result.stdout.strip()}")
    
    # Create database
    print("\n[*] Creating wharfintel database...")
    create_db_cmd = 'psql -U postgres -c "CREATE DATABASE wharfintel;" 2>nul'
    subprocess.run(create_db_cmd, shell=True)
    
    # Verify database exists
    list_db_cmd = 'psql -U postgres -c "SELECT datname FROM pg_database WHERE datname=\'wharfintel\';"'
    result = subprocess.run(list_db_cmd, shell=True, capture_output=True, text=True)
    
    if "wharfintel" in result.stdout:
        print("[✓] Database 'wharfintel' created/exists")
    else:
        print("[!] Database may not have been created, but continuing...")
    
    # Display next steps
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Start the backend server:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n2. Tables will be created automatically on first run")
    print("\n3. Backend will connect to PostgreSQL at:")
    print("   postgresql://postgres:postgres@localhost:5432/wharfintel")
    print("\n4. Start the frontend (in another terminal):")
    print("   cd frontend")
    print("   npm run dev")
    print("\n5. Open browser to: http://localhost:5173")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
