import sqlite3
from pathlib import Path

# Path to the database file
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            address TEXT,
            kids INTEGER DEFAULT 0,
            job TEXT,
            marital_status TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully at:", DB_PATH)

