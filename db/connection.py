import sqlite3

# Creates a connection to file, if it doesn't exist create it | Always close connection! 
def create_connection(db_file):
    """
    Create a database connection at specific location.

    Args:
        db_file: filepath for database file

    Returns:
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version, conn)
    except Exception as e:
        print(e)
    
    return conn
    """Close the connection after using it."""

if __name__ == "__main__":
    create_connection("bookstore.db")