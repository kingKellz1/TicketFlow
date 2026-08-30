import sqlite3


def initialize_database():
    db_connection = sqlite3.connect("data/ticketflow.db")
    db_cursor = db_connection.cursor()

    # Create a table named 'users' with eleven columns
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            account_type TEXT NOT NULL,
            department TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # Save the changes to the database file
    db_connection.commit()

    # Close the cursor and connection properly
    db_cursor.close()
    db_connection.close()