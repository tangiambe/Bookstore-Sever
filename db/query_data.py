from connection import create_connection

""" ==========  All QUERIES  =========== """

def all_books(conn):
    sql = "SELECT * FROM book"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def all_authors(conn):
    sql = "SELECT * FROM author"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def all_categories(conn):
    sql = "SELECT * FROM category"
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def get_book_id(conn,value=None):
    cursor = conn.cursor()
    sql = "SELECT book_id from bookauthor where author_id = ?"
    cursor.execute(sql, [value])
    return cursor.fetchone()

def update_author(conn, value=None, author_id=None):
    cursor = conn.cursor()
    sql = "UPDATE author SET name = ? WHERE id = ?"
    cursor.execute(sql, [value, author_id])
    conn.commit()
    return cursor.fetchone()

def update_category(conn, value=None, category_id=None):
    cursor = conn.cursor()
    sql = "UPDATE category SET name = value WHERE id = ?"
    cursor.execute(sql, [value])
    conn.commit()
    return cursor.fetchone()

def update_bookauthor(conn, value=None, column=None):
    cursor = conn.cursor()
    sql = "UPDATE bookauthor SET column = value WHERE column = ?"
    cursor.execute(sql, [value])
    conn.commit()
    return cursor.fetchone()

def update_book(conn, value=None, column=None):
    cursor = conn.cursor()
    sql = "UPDATE book SET column = value WHERE column = ?"
    cursor.execute(sql, [value])
    conn.commit()
    return cursor.fetchone()

def delete_author(conn, value=None):
    cursor = conn.cursor()
    """sql = "DELETE FROM book WHERE id = ?"
    cursor.execute(sql, [book_id])
    conn.commit()"""

    sql = "DELETE FROM author WHERE id = ?"
    cursor.execute(sql, [value])
    conn.commit()

    sql = "DELETE FROM bookauthor WHERE author_id = ?"
    cursor.execute(sql, [value])
    conn.commit()

    return cursor.fetchone()


def delete_category(conn, value=None,column=None):
    cursor = conn.cursor()
    sql = "DELETE FROM category WHERE column = ?"
    cursor.execute(sql, [value])

    conn.commit()
    return cursor.fetchone()

def delete_bookauthor(conn, value=None, column=None):
    cursor = conn.cursor()
    sql = "DELETE FROM bookauthor WHERE column = ?"
    cursor.execute(sql, [value])
    conn.commit()
    return cursor.fetchone()

def delete_book(conn, value=None, column=None):
    cursor = conn.cursor()
    sql = "DELETE FROM book WHERE column = ?"
    cursor.execute(sql, [value])
    conn.commit()
    return cursor.fetchone()

def select_book(conn, book_id):
    sql = "SELECT * FROM book WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(sql, [book_id])
    return cursor.fetchone()

def select_author(conn, value=None, column=None):
    cursor = conn.cursor()

    if column == "name":
        sql = "SELECT id, name FROM author WHERE name = ?"
        cursor.execute(sql, [value])

    elif column == "id":
        sql = "SELECT id, name FROM author WHERE id = ?"
        cursor.execute(sql, [value])

    else:
        sql = "SELECT id, name FROM author"
        cursor.execute(sql)

    return cursor.fetchone()


def select_category(conn, value=None, column=None):
    cursor = conn.cursor()

    if column == "name":
        sql = "SELECT id, name FROM category WHERE name = ?"
        cursor.execute(sql, [value])

    elif column == "id":
        sql = "SELECT id, name FROM category WHERE id = ?"
        cursor.execute(sql, [value])

    else:
        sql = "SELECT id, name FROM category"
        cursor.execute(sql)

    return cursor.fetchone()



def main():
    database = "bookstore.db"
    conn = create_connection(database)


if __name__ == "__main__":
    main()
