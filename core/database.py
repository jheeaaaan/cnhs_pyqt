import sys
from pathlib import Path

import psycopg2
import psycopg2.pool
from dotenv import dotenv_values


class DatabaseConfigurationError(RuntimeError):
    pass


def _get_base_dir():
    if getattr(sys, 'frozen', False):
        # Running as bundled .exe — look next to the executable
        return Path(sys.executable).parent
    else:
        # Running as script — look in project root
        return Path(__file__).resolve().parent.parent

BASE_DIR = _get_base_dir()
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
            'Create a .env file and set DB_PASSWORD.'
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
    return _get_pool().getconn()

def release_connection(conn):
    _get_pool().putconn(conn)

def execute(sql, params=None, fetch=None):
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