import sqlite3

def create_connection():
    """Create a database connection to a SQLite database."""
    return sqlite3.connect("ticketflow.db")

def create_users_table(connection):
    """Create the users table if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            department TEXT NOT NULL CHECK(department IN ('HR', 'Operations', 'Marketing', 'Sales')),
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Employee')),
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER NOT NULL DEFAULT 0 CHECK(is_active IN (0, 1))
            );
            ''')
    connection.commit()
    
def initialize_database():
    """Initialize the database by creating necessary tables."""
    connection = create_connection()
    create_users_table(connection)
    connection.close()