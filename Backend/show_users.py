import sqlite3
import os

# Check if database exists in current directory
db_path = "safeher.db"
if not os.path.exists(db_path):
    print(f"Error: {db_path} not found in this directory. Make sure you run this script from the Backend folder.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT id, name, username, email, hash_password FROM user_table;")
    users = cursor.fetchall()
    
    if not users:
         print("No users found in user_table.")
    else:
         print(f"{'ID':<5} | {'Name':<15} | {'Username':<15} | {'Email':<25} | {'Password Hash (Truncated)':<30}")
         print("-" * 98)
         for user in users:
             truncated_hash = user[4][:30] + "..." if len(user[4]) > 30 else user[4]
             print(f"{user[0]:<5} | {user[1]:<15} | {user[2]:<15} | {user[3]:<25} | {truncated_hash:<30}")
except sqlite3.OperationalError as e:
    print(f"Database error: {e}")
finally:
    conn.close()
