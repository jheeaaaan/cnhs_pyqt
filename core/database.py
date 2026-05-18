# core/database.py
import psycopg2
import psycopg2.pool
import bcrypt

_env = {}
try:
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                _env[k.strip()] = v.strip()
except FileNotFoundError:
    pass

_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=1, maxconn=10,
    dbname=_env.get('DB_NAME', 'cnhs_db'),
    user=_env.get('DB_USER', 'postgres'),
    password=_env.get('DB_PASSWORD', '0909231404217'),
    host=_env.get('DB_HOST', 'localhost'),
    port=_env.get('DB_PORT', '5432'),
)

def get_connection():
    """Get a connection from the pool. Call release_connection() when done."""
    return _pool.getconn()

def release_connection(conn):
    """Return connection to pool."""
    _pool.putconn(conn)

def execute(sql, params=None, fetch=None):
    """
    Convenience helper. fetch can be: 'one', 'all', or None (for INSERT/UPDATE/DELETE).
    Handles connection get/release automatically.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if fetch == 'one':
                return cur.fetchone()
            elif fetch == 'all':
                return cur.fetchall()
            else:
                conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        release_connection(conn)