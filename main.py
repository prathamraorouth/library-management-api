from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Library Management API")

# Database
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    available INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")
conn.commit()

# Models
class Book(BaseModel):
    title: str
    author: str

class User(BaseModel):
    name: str

class Borrow(BaseModel):
    user_id: int
    book_id: int

# Routes
@app.post("/books")
def add_book(book: Book):
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
    conn.commit()
    return {"message": "Book added successfully"}

@app.post("/users")
def add_user(user: User):
    cursor.execute("INSERT INTO users (name) VALUES (?)", (user.name,))
    conn.commit()
    return {"message": "User registered successfully"}

@app.post("/borrow")
def borrow_book(borrow: Borrow):
    cursor.execute("SELECT available FROM books WHERE id = ?", (borrow.book_id,))
    row = cursor.fetchone()
    if not row or row[0] == 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    cursor.execute("INSERT INTO borrows (user_id, book_id) VALUES (?, ?)", (borrow.user_id, borrow.book_id))
    cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (borrow.book_id,))
    conn.commit()
    return {"message": "Book borrowed successfully"}

@app.post("/return/{book_id}")
def return_book(book_id: int):
    cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
    cursor.execute("DELETE FROM borrows WHERE book_id = ?", (book_id,))
    conn.commit()
    return {"message": "Book returned successfully"}
