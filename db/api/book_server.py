from flask import Flask, request, jsonify
from connection import create_connection
import query_data as db
import create_data as create



app = Flask(__name__)

"""@app.route("/")
def home():
    return render_template("index.html")"""

"""@app.route("/api")
def api_home():
    return jsonify({
        "greeting":"Welcome to the book API",
        "See all Books": ["/api/book", "GET"],
        "Add New Books": ["/api/book", "POST"]
        })"""

@app.route("/books")
def books_page():
    conn = create_connection("bookstore.db")
    books = qd.all_books(conn)
    results = []
    for book in books:
        author = qd.select_author(conn, book[3], "id")
        category = qd.select_category(conn, book[4], "id")
        results.append({
            "name":book[1],
            "published": book[2],
            "author": author[1],
            "category": category[1]
        })
    return render_template("books.html", books = results)


@app.route("/api/book", methods=["GET", "POST"])
def book():

    if request.method == "GET":
        conn = create_connection("bookstore.db")
        books = qd.all_books(conn)
        results = []
        for book in books:
            author = qd.select_author(conn, book[3], "id")
            category = qd.select_category(conn, book[4], "id")
            results.append({
                "name":book[1],
                "published": book[2],
                "author": author[1],
                "category": category[1]
            })
        conn.close()
        return results, 200
    
    elif request.method == "POST":
        conn = create_connection("bookstore.db")
        if request.form:
            book = create.insert_book(conn,{
                "name":request.form["name"],
                "author":request.form["author"],
                "category":request.form["category"],
                "published":request.form["published"],
            })
            conn.close()
            return render_template("index.html"), 201
        else:
            book = create.insert_book(conn, request.json)
            conn.close()
            return jsonify(book), 201

@app.route("/api/book/<book_id>", methods=["GET", "PUT", "DELETE"])
def book_by_id(book_id):
    if request.method == "GET":
        conn = create_connection("bims.db")
        book = qd.select_book(conn, book_id)
        if book:
            author = qd.select_author(conn, book[3], "id")
            category = qd.select_category(conn, book[4], id)
            result = {
                    "name":book[1],
                    "published": book[2],
                    "author": author[1],
                    "category": category[1]
            }
            conn.close()
            return result, 200
        else:
            return f"book with id {book_id} not found", 204
    elif request.method == "PUT":
       # TODO: implement book query
       # book = request.json()
       # update_book(book_id, book)
       return f"Updated book with id: {book_id}"
    elif request == "DELETE":
        # TODO: implement delete book
        # delete_book(book_id)
        return f"deleted book with id {book_id}"

if __name__ == "__main__":
    app.run(debug=True)