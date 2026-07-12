import sqlite3
import os

db_path = r'C:\Users\Dell\Desktop\Safe-Her-Complete\Safe-Her\Backend\safeher.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Found tables in database:", tables)
    
    for table in tables:
        if table.startswith("sqlite_"):
            continue
        try:
            print(f"Clearing table '{table}'...")
            cursor.execute(f"DELETE FROM {table};")
            print(f"Successfully cleared '{table}'.")
        except Exception as e:
            print(f"Error clearing '{table}':", e)
            
    conn.commit()
    conn.close()
    print("Database cleanup finished.")
else:
    print(f"Database not found at {db_path}")
