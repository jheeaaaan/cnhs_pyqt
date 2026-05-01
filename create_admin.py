# create_admin.py
import bcrypt
from core.database import get_connection, release_connection

username = input("Enter username: ").strip()
password = input("Enter password: ").strip()

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

conn = get_connection()
try:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO auth_user (username, password_hash, is_active) VALUES (%s, %s, TRUE)",
            (username, hashed)
        )
    conn.commit()
    print(f"✅ Admin '{username}' created successfully!")
except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
finally:
    release_connection(conn)