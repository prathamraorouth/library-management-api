from fastapi import FastAPI

app = FastAPI(title="Library Management API")

# Example in-memory "database"
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"}
]

@app.get("/")
def home():
    return {"message": "Welcome to the Library Management API"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return {"error": "Book not found"}

@app.post("/books")
def add_book(book: dict):
    new_id = len(books) + 1
    book["id"] = new_id
    books.append(book)
    return book
