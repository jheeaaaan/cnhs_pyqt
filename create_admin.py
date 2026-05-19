# change_password.py
import bcrypt
from core.database import get_connection, release_connection

def change_password():
    username = input("Enter the username you want to update: ").strip()
    new_password = input("Enter the NEW password: ").strip()

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # We use UPDATE instead of INSERT
            cur.execute(
                "UPDATE auth_user SET password_hash = %s WHERE username = %s",
                (hashed, username)
            )
            
            if cur.rowcount > 0:
                conn.commit()
                print(f"✅ Success! Password for '{username}' has been updated.")
            else:
                print(f"⚠️ User '{username}' not found. No changes made.")
                
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        release_connection(conn)

if __name__ == "__main__":
    change_password()