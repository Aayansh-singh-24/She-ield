import sqlite3
import os

db_path = r'C:\Users\Dell\Desktop\Safe-Her-Complete\Safe-Her\Backend\safeher.db'
if os.path.exists(db_path):
    print("Database found. Modifying tables...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns in otp_verification
    cursor.execute("PRAGMA table_info(otp_verification)")
    columns = [row[1] for row in cursor.fetchall()]
    
    new_cols = {
        'name': 'TEXT',
        'username': 'TEXT',
        'hash_password': 'TEXT'
    }
    
    for col, col_type in new_cols.items():
        if col not in columns:
            print(f"Adding column '{col}' to table 'otp_verification'")
            cursor.execute(f"ALTER TABLE otp_verification ADD COLUMN {col} {col_type};")
        else:
            print(f"Column '{col}' already exists in table 'otp_verification'")
            
    conn.commit()
    conn.close()
    print("Database modification finished successfully.")
else:
    print("Database not found. Columns will be created automatically on application start.")
