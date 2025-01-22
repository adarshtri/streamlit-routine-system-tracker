import sqlite3

from src.utils.helper import deprecated

DB_NAME = "login.db"
LOGGEDIN_USERS_TABLE_NAME = "loggedin_users"


# Database and table initialization
def initialize_database():
    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {LOGGEDIN_USERS_TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

initialize_database()

@deprecated
def is_a_user_logged_in():
    """
    Checks if a user is logged in.

    Returns:
        bool: True if the table is not empty, False otherwise.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Query to count rows in the table
    cursor.execute(f"SELECT COUNT(*) FROM {LOGGEDIN_USERS_TABLE_NAME}")
    row_count = cursor.fetchone()[0]

    conn.close()

    if row_count == 0:
        return False
    return True


@deprecated
def save_user(username):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if is_a_user_logged_in():
            return

        # Insert the username into the table
        cursor.execute(f"""
            INSERT INTO {LOGGEDIN_USERS_TABLE_NAME} (username)
            VALUES (?)
        """, (username,))

        # Commit the changes and close the connection
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    finally:
        conn.close()


@deprecated
def get_current_user():
    """
    Fetches the username of the most recent entry in the 'loggedin_users' table.

    Returns:
        str: The username of the most recent entry, or None if no users are present.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(f"SELECT username FROM {LOGGEDIN_USERS_TABLE_NAME} ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the username
    return None


@deprecated
def delete_user(username):
    """
    Deletes a user entry from the 'loggedin_users' table by username.

    Args:
        username (str): The username of the user to delete.

    Returns:
        bool: True if the user was deleted successfully, False if the user was not found.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Delete the user entry by username
    cursor.execute(f"DELETE FROM {LOGGEDIN_USERS_TABLE_NAME} WHERE username = ?", (username,))

    conn.commit()

    # Check if any rows were deleted
    if cursor.rowcount > 0:
        conn.close()
        return True  # User deleted successfully
    else:
        conn.close()
        return False  # User not found or not deleted