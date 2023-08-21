from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import re
import bcrypt
from bson import ObjectId

 
app = Flask(__name__)

app.secret_key = 'xyzsdfg'

# Initialize MongoDB client
client = MongoClient("mongodb+srv://cody:team2password@books.ondwxvg.mongodb.net/")
db = client.get_database("bookstore_db")
users_collection = db.user
books_collection = db.book
categories_collection = db.category
authors_collection = db.author
bookauthor_collection = db.bookauthor

def is_user_logged_in():
    return 'user_id' in session

@app.route('/index')
def index():
    first_name = None
    last_name = None
    user_logged_in = is_user_logged_in()
    if user_logged_in:
        # Fetch the username based on user_id
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')
            last_name = user.get('last_name')
    return render_template('index.html', user_logged_in=user_logged_in, first_name=first_name, last_name=last_name)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    registration_success = request.args.get('registration_success')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid credentials')
    return render_template('login.html', registration_success=registration_success)

 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    first_name = None
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([first_name, last_name, username, email, password]):
            message = 'Please fill out all the fields!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif users_collection.find_one({'email': email}):
            message = 'Account already exists!'
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': hashed_password  # Store the hashed password as bytes
            }
            users_collection.insert_one(user_data)
            message = 'You have successfully registered!'
            
            return redirect(url_for('login', registration_success=True))

    return render_template('register.html', message=message, first_name=first_name)

#######



@app.route("/search_books", methods=["GET"])
def search_books():
    user_logged_in = is_user_logged_in()
    first_name = None
    if user_logged_in:
        # Fetch the username based on user_id
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')

    # Retrieve categories from categories_collection
    categories = categories_collection.find()
    
    return render_template("search_books.html", user_logged_in=user_logged_in, first_name=first_name, categories=categories)


@app.route("/create_book", methods=["GET", "POST"])
def create_book():
    first_name = None
    user_logged_in = is_user_logged_in()
    if user_logged_in:
        # Fetch the first_name based on user_id
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')

    if not user_logged_in:
        return redirect(url_for('login'))

    if request.method == "POST":
        title = request.form.get("title")
        category_id = int(request.form.get("category"))
        id = int(request.form.get("id"))
        price = float(request.form.get("price"))
        year = int(request.form.get("year"))
        quantity = int(request.form.get("quantity"))

        # Create the book data
        book_data = {
            "title": title,
            "price": price,
            "year": year,
            "quantity": quantity,
            "rating": "0",  # You can add a default rating
            "category_id": category_id,
            "id": id
        }
        book_id = books_collection.insert_one(book_data).inserted_id

        # Connect the author to the book in bookauthor_collection
        bookauthor_collection.insert_one({"book_id": book_id})
        message = 'Book created successfully!'

        categories = categories_collection.find()
        return render_template("create_book.html", message=message, categories=categories, user_logged_in=user_logged_in, first_name=first_name)

    categories = categories_collection.find()
    return render_template("create_book.html", categories=categories, user_logged_in=user_logged_in, first_name=first_name)


@app.route("/search_results", methods=["GET"])
def search_results():
    user_logged_in = is_user_logged_in()
    first_name = None
    if user_logged_in:
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')
    
    search_term = request.args.get('searchTerm')
    category = request.args.get('category')
    
    # Build the MongoDB query based on search_term and category (if provided)
    query = {}
    if search_term:
        query["$or"] = [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"id": {"$regex": search_term, "$options": "i"}}
        ]
    if category:
        query["category_id"] = int(category)
    
    # Retrieve book data from MongoDB based on the query
    books = books_collection.find(query)
    
    return render_template("search_results.html", books=books, user_logged_in=user_logged_in, first_name=first_name)

@app.route('/book_info/<int:book_id>' , methods=["GET"])
def book_info(book_id):
    user_logged_in = is_user_logged_in()
    first_name = None
    if user_logged_in:
        # Fetch the first_name based on user_id
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')
    
    search_term = request.args.get('searchTerm')
    category = request.args.get('category')
    
    # Build the MongoDB query based on search_term and category (if provided)
    query = {'id':book_id}
    
    
    # Retrieve book data from MongoDB based on the query
    books = books_collection.find(query)
    print(type(books))
    return render_template("book_info.html", books=books, user_logged_in=user_logged_in, first_name=first_name)

@app.route('/search_results/<int:book_id>/delete')
def delete_book(book_id):
    print(book_id)
    first_name = None
    user_logged_in = is_user_logged_in()
    if user_logged_in:
        # Fetch the username based on user_id
        user = users_collection.find_one({'_id': ObjectId(session['user_id'])})
        if user:
            first_name = user.get('first_name')

    # if not user_logged_in:
    #     return redirect(url_for('login'))
    
    query = {'id':book_id}

    # Build the MongoDB query based on search_term and category (if provided)
    # Retrieve book data from MongoDB based on the query
    books = books_collection.delete_one(query)

    return render_template('search_books.html', user_logged_in=user_logged_in, first_name=first_name)


@app.route('/update_book/<int:book_id>', methods=["POST"])
def update_book(book_id):
    if request.method == 'POST':
        field_val = request.form.get('fieldVal')
        field_input = request.form.get('fieldInput')
        
        # Construct the filter and update query
        filter_query = {'id': book_id}
        update_query = {'$set': {field_val: field_input}}
        
        # Update the book using the constructed queries
        books_collection.update_one(filter_query, update_query)
        
        return redirect(url_for('search_results'))
    
    # Fetch the book details for the given book_id
    book = books_collection.find_one({'id': book_id})
    
    return render_template('update_book.html', book=book)


   
if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)