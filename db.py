import sqlite3
from config import Config

# Connect to the SQLite database
def get_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create all required tables
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Visitors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        visitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        gender TEXT NOT NULL,
        address TEXT NOT NULL,
        employee_name TEXT NOT NULL,
        department TEXT NOT NULL,
        purpose TEXT NOT NULL,
        visit_date TEXT NOT NULL,
        visit_time TEXT NOT NULL,
        id_proof TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    # Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        department TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # Check-In / Check-Out Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkin_checkout (
        check_id INTEGER PRIMARY KEY AUTOINCREMENT,
        visitor_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        duration TEXT,
        FOREIGN KEY(visitor_id)
        REFERENCES visitors(visitor_id)
    )
    """)

    conn.commit()
    conn.close()