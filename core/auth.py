# core/auth.py
import bcrypt
from core.database import execute
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str

_current_user = None

def login(username: str, password: str) -> tuple:
    global _current_user
    row = execute(
        'SELECT id, username, password_hash, is_active FROM auth_user WHERE username=%s',
        (username,), fetch='one'
    )
    if not row:
        return False, 'Username not found.'
    _id, _user, hashed, is_active = row
    if not is_active:
        return False, 'This account is inactive.'
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        _current_user = User(_id, _user)
        return True, _current_user
    return False, 'Incorrect password.'

def logout():
    global _current_user
    _current_user = None

def get_current_user() -> User:
    return _current_user

def change_password(user_id: int, old_password: str, new_password: str) -> tuple:
    row = execute(
        'SELECT password_hash FROM auth_user WHERE id=%s',
        (user_id,), fetch='one'
    )
    if not row:
        return False, 'User not found.'
    if not bcrypt.checkpw(old_password.encode(), row[0].encode()):
        return False, 'Current password is incorrect.'
    new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    execute('UPDATE auth_user SET password_hash=%s WHERE id=%s', (new_hash, user_id))
    return True, 'Password changed successfully.'