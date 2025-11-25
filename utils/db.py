import sqlite3
import os

# Path to the SQLite database (same as in app.py)
DB_PATH = os.path.join("instance", "shop.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock INTEGER,
    category TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    items TEXT,
    total REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def get_connection():
    """Return a new database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables and a default admin user."""
    os.makedirs("instance", exist_ok=True)

    conn = get_connection()
    cur = conn.cursor()

    # Create tables
    cur.executescript(SCHEMA_SQL)

    # Default admin user
    cur.execute(
        """
        INSERT OR IGNORE INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
        """
    )

    conn.commit()
    conn.close()
    print("Database initialized with default admin (admin/admin123).")


if __name__ == "__main__":
    init_db()
