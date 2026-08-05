import os
import sqlite3
import hashlib

# Use /tmp on Vercel Serverless environment, local file otherwise if writable
if 'VERCEL' in os.environ or os.environ.get('VERCEL_ENV'):
    DB_PATH = '/tmp/pswx_database.db'
else:
    local_db = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pswx_database.db'))
    try:
        db_dir = os.path.dirname(local_db)
        if not os.access(db_dir, os.W_OK):
            DB_PATH = '/tmp/pswx_database.db'
        else:
            DB_PATH = local_db
    except Exception:
        DB_PATH = '/tmp/pswx_database.db'


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Computes SHA-256 cryptographic hash for password storage & admin privacy view."""
    salt = "PSWX_CYBER_SALT_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            google_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Saved Passwords Vault Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            password_hash TEXT NOT NULL,
            masked_password TEXT NOT NULL,
            health_score INTEGER NOT NULL,
            category TEXT NOT NULL,
            entropy_bits REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Ensure Admin Account exists (Name: 'admin', Email: 'admin@pswx.ai', Password: 'pass@123')
    admin_pass_hash = hash_password('pass@123')
    cursor.execute('SELECT * FROM users WHERE email = ? OR name = ?', ('admin@pswx.ai', 'admin'))
    existing_admin = cursor.fetchone()

    if existing_admin:
        cursor.execute('''
            UPDATE users 
            SET name = 'admin', email = 'admin@pswx.ai', password_hash = ?, role = 'admin'
            WHERE id = ?
        ''', (admin_pass_hash, existing_admin['id']))
    else:
        cursor.execute('''
            INSERT INTO users (email, name, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin@pswx.ai', 'admin', admin_pass_hash, 'admin'))

    # Create default Demo User Account if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('user@pswx.ai',))
    if not cursor.fetchone():
        user_pass_hash = hash_password('User@PSWX2026!')
        cursor.execute('''
            INSERT INTO users (email, name, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('user@pswx.ai', 'Demo Security User', user_pass_hash, 'user'))

    conn.commit()
    conn.close()
