#!/usr/bin/env python
"""
Database Viewer Script
Shows all users with their authentication data (hashes and salts)
Useful for project documentation and verification
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "wharfintel.db"

def view_database():
    """Display all database tables and their contents"""
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        print("\n" + "="*80)
        print("WHARFINTEL DATABASE - USER AUTHENTICATION TABLE")
        print("="*80 + "\n")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            print(f"\n📋 TABLE: {table_name}")
            print("-" * 80)
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print(f"{'Column':<25} {'Type':<15} {'Nullable':<10} {'Key':<10}")
            print("-" * 80)
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                nullable = "YES" if col[3] == 0 else "NO"
                is_key = "PRIMARY KEY" if col[5] == 1 else ""
                print(f"{col_name:<25} {col_type:<15} {nullable:<10} {is_key:<10}")
            
            # Get data
            print("\n📊 DATA:")
            print("-" * 80)
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if rows:
                # Print headers
                col_names = [desc[0] for desc in cursor.description]
                col_widths = [max(len(name), 30) for name in col_names]
                
                header = " | ".join([name.ljust(width) for name, width in zip(col_names, col_widths)])
                print(header)
                print("-" * 80)
                
                # Print data
                for row in rows:
                    row_str = " | ".join([str(val)[:col_widths[i]].ljust(col_widths[i]) if val else "NULL".ljust(col_widths[i]) for i, val in enumerate(row)])
                    print(row_str)
            else:
                print("(No data)")
            
            print()
        
        conn.close()
        print("\n" + "="*80)
        print("✅ Database view complete")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    view_database()
