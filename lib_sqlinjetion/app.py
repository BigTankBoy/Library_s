from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'blind_library.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    cur = db.execute("SELECT DISTINCT genre FROM books")
    genres = cur.fetchall()
    return render_template("index.html", genres=genres)

@app.route('/genre')
def genre():
    genre = request.args.get('genre', '')
    db = get_db()
    cur = db.execute("SELECT id, title FROM books WHERE genre=?", (genre,))
    books = cur.fetchall()
    return render_template("genre.html", books=books, genre=genre)

@app.route('/book/<int:book_id>')
def book(book_id):
    db = get_db()
    cur = db.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cur.fetchone()
    return render_template("book.html", book=book)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    db = get_db()
    try:
        query = f"SELECT title AS result FROM books WHERE title LIKE '%{q}%'"
        books = db.execute(query).fetchall()
    except:
        books = []
    return render_template("search.html", books=books, query=q)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)