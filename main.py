from flask import Flask, request, redirect, render_template
import sqlite3
from contextlib import closing


def display(): # Grab the books in database and return them
    conn = sqlite3.connect("books.sqlite") # Local storage connection
    c = conn.cursor()
    conn.row_factory = sqlite3.Row
    try:
        with closing(conn.cursor()) as c:   # Connect and store the books
            query = '''SELECT book_name, author, owner, holder FROM Book'''
            c.execute(query)
            books = c.fetchall()
    except sqlite3.OperationalError as e:
        books = None
    return books

def find(title):    # Obtain the books with a given title and return them
    conn = sqlite3.connect("books.sqlite")
    c = conn.cursor()
    query = '''SELECT book_name, author, owner, holder
        FROM Book
        WHERE book_name=?'''
    c.execute(query, (title,))
    books = c.fetchall()
    if len(books) > 0:  # Ensure books are present
        return books
    else:
        return 0

def findDuplicate(title, owner): # Look for duplicates, checks before adding a book
    conn = sqlite3.connect("books.sqlite")
    c = conn.cursor()
    query = '''SELECT book_name, author, owner, holder
        FROM Book
        WHERE book_name=? AND owner=?'''
    c.execute(query, (title,owner,))
    books = c.fetchall() # Catches all duplicates and returns them
    if len(books) > 0:
        return books
    else:
        return 0
    
def findRemove(title): # Check to see if the book exists before removing
    conn = sqlite3.connect("Books.sqlite")
    c = conn.cursor()
    query = '''SELECT book_name, author, owner, holder
        FROM Book
        WHERE book_name=?'''
    c.execute(query, (title,))
    books = c.fetchall()
    if len(books) > 0:
        return True
    else:
        return False

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html") # home page load

@app.route('/displayBooks.html') # Displays all books page
def displayBooks():
    books = display()
    return render_template("displayBooks.html", books=books)

@app.route('/addBook.html') # Add a book form page
def addBook():
    return render_template("addBook.html")

@app.route('/add_book',methods=['POST'] )
def add(): 
    title = request.form.get('title') # Grabs the details from the form
    author = request.form.get('author')
    owner = request.form.get('owner')
    conn = sqlite3.connect("books.sqlite")
    c = conn.cursor()
    conn.row_factory = sqlite3.Row
    books = findDuplicate(title,owner)
        
    if title and author and owner:
        if books == 0:
            with closing(conn.cursor()) as c:
                sql = '''INSERT INTO Book 
                    (book_name, owner, author, holder)
                        VALUES 
                        (?, ?, ?, ?)'''
                c.execute(sql, (title, owner, author, owner))
                conn.commit()  
        else:
            return render_template("exists.html")
    return render_template("/")

@app.route('/findBook.html') # Find a book page
def findBook():
    return render_template("findBook.html")

@app.route('/find_book', methods=['POST'])  # Find a book function
def finding():
    title = request.form.get('title')
    books = find(title)
    if books == 0:
        return render_template('notFound.html')
    return render_template('findBook.html', books=books)

@app.route('/loanBook.html')    # Loan book page
def loanBook():
    return render_template("loanBook.html")

@app.route('/loan_book', methods=['POST']) # Loan book SQL
def loan():
    owner = request.form.get('owner')
    title = request.form.get('title')
    holder = request.form.get('holder')
    conn = sqlite3.connect("books.sqlite")
    c = conn.cursor()
    conn.row_factory = sqlite3.Row
    if title and holder and owner:
        with closing(conn.cursor()) as c:
            sql = '''UPDATE Book
                SET holder = ?                    
                WHERE book_name = ? AND owner = ?'''
            c.execute(sql, (holder, title, owner))
            conn.commit()
        return redirect("/")
    return "Wrong Input"

@app.route('/removeBook.html')  # Remove book page
def removeBook():
    return render_template("removeBook.html")

@app.route('/remove_book', methods=['POST']) # Remove a book
def remove():
    owner = request.form.get('owner')
    title = request.form.get('title')
    if findRemove(title):
        conn = sqlite3.connect("books.sqlite")
        c = conn.cursor()
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as c:
            sql =  '''DELETE FROM Book
                  WHERE book_name = ? AND owner = ?'''                
            c.execute(sql, (title,owner,))
            conn.commit()
        return render_template('/')
    return render_template("notFound.html")

if __name__ == "__main__": # On startup run
    conn = sqlite3.connect("books.sqlite")
    app.run(debug=True)
    conn.close()
