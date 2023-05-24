import sqlite3
from sqlite3 import Error

from connection import create_connection


def create_table(conn, create_table_sql):
    """
    Make a table with the specified statement

    Args:
        conn = Connection Object
        create_table_sql = SQL statement about table creation
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    print("Running main")
    database = "bims.db"

    make_author_table = """
                        CREATE TABLE IF NOT EXISTS author
                        (
                            id integer PRIMARY KEY,
                            name VARCHAR(255) NOT NULL
                        );
                        """

    make_category_table = """
                        CREATE TABLE IF NOT EXISTS category
                        (
                            id integer PRIMARY KEY,
                            name VARCHAR(255) NOT NULL
                        );
                        """

    make_book_table = """
                    CREATE TABLE IF NOT EXISTS book
                    (
                        id integer PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        published DATE,
                        author_id integer NOT NULL,
                        category_id integer NOT NULL,
                        FOREIGN KEY (author_id)
                            REFERENCES author (id),
                        FOREIGN KEY (category_id)
                            REFERENCES category (id)
                    );
                    """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, make_author_table)
        create_table(conn, make_category_table)
        create_table(conn, make_book_table)

    else:
        print("Aw geez, something's wrong with your db connection!")


if __name__ == "__main__":
    main()
