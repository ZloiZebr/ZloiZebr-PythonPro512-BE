
from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel

app = FastAPI()

books = []

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

class NewBook(BaseModel):
    title: str
    author: str
    year: int

@app.get("/books")
async def get_books(author: str | None = None) -> list:
    if not author:
        return books
    sorted_books = []
    for b in books:
        if author == b.author:
            sorted_books.append(b)
    if len(sorted_books) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return sorted_books
    

@app.post("/books",status_code = status.HTTP_201_CREATED)
async def create_new_book(book_create:NewBook) -> Book:
    new_id = len(books) + 1 if books else 1
    new_book = Book(
            id = new_id,
            title = book_create.title,
            author = book_create.author, 
            year = book_create.year,
        )
    books.append(new_book)
    return new_book

@app.put("/books/{id}")
async def book_update(
    id: int,
    book_update:Book,
) -> Book:
    for i, b in enumerate(books):
        if b.id == id:
            updated_book = Book(
                id=b.id,
                title=book_update.title,
                author=book_update.author,
                year=book_update.year,
            )
            books[i] = updated_book
            return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def book_delete(id: int):
    for i, b in enumerate(books):
        if b.id == id:
            books.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
    

@app.get("/books/{id}")
async def get_book_id(
    id: int
) -> Book:
    for b in books:
        if id == b.id:
            return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")