from pathlib import Path

import psycopg2
import psycopg2.pool
from dotenv import dotenv_values


class DatabaseConfigurationError(RuntimeError):
    pass


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'

_env = dotenv_values(ENV_PATH) if ENV_PATH.exists() else {}
_pool = None


def _db_config():
    return {
        'dbname': _env.get('DB_NAME') or 'cnhs_db',
        'user': _env.get('DB_USER') or 'postgres',
        'password': _env.get('DB_PASSWORD') or '',
        'host': _env.get('DB_HOST') or 'localhost',
        'port': _env.get('DB_PORT') or '5432',
    }


def _validate_config(config):
    if not ENV_PATH.exists():
        raise DatabaseConfigurationError(
            f'Database settings file not found: {ENV_PATH}. '
            'Create a .env file from .env.example and set DB_PASSWORD.'
        )
    if not config['password'] or config['password'] == 'your_postgres_password':
        raise DatabaseConfigurationError(
            'DB_PASSWORD is missing in .env. Set it to your PostgreSQL password.'
        )


def _get_pool():
    global _pool
    if _pool is None:
        config = _db_config()
        _validate_config(config)
        _pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            **config,
        )
    return _pool

def get_connection():
    """Get a connection from the pool. Call release_connection() when done."""
    return _get_pool().getconn()

def release_connection(conn):
    """Return connection to pool."""
    _get_pool().putconn(conn)

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
