from fastapi import FastAPI, HTTPException, Depends, Query, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import Book, get_db
from typing import List, Optional
from schemas import BookResponse, BookCreate, BookUpdate

app = FastAPI(title="Books API")


# -----------------------------------------------------------------------------
# Create a new book
# -----------------------------------------------------------------------------
@app.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate,
                db: Session = Depends(get_db)
                ):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# -----------------------------------------------------------------------------
# Retrieve all books
# -----------------------------------------------------------------------------
@app.get("/books/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """
    Create a new book entry in the database.
    """
    result = db.execute(select(Book).order_by(Book.id))
    result = result.scalars().all()
    return result

# -----------------------------------------------------------------------------
# Retrieve a single book by ID
# -----------------------------------------------------------------------------
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int,
             db: Session = Depends(get_db)
             ):
    result = db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

# -----------------------------------------------------------------------------
# Delete a book by ID
# -----------------------------------------------------------------------------
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int,
                db: Session = Depends(get_db)
                ):
    """
    Retrieve a list of all books stored in the database.
    """
    stmt = delete(Book).where(Book.id == book_id).returning(Book.id)
    result = db.execute(stmt)
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.commit()

# -----------------------------------------------------------------------------
# Update a book by ID
# -----------------------------------------------------------------------------
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int,
                book_update: BookUpdate,
                db: Session = Depends(get_db)
                ):
    """
    Retrieve a single book by its ID.
    """
    result = db.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# -----------------------------------------------------------------------------
# Search books by title, author, or year
# -----------------------------------------------------------------------------
@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
        title: Optional[str] = Query(None, description="Filter by book title"),
        author: Optional[str] = Query(None, description="Filter by book author"),
        year: Optional[int] = Query(None, description="Filter by publication year"),
        db: Session = Depends(get_db)
):
    """
    Delete a book by ID.
    """
    stmt = select(Book)

    if title:
        stmt = stmt.where(Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(Book.author.ilike(f"%{author}%"))
    if year:
        stmt = stmt.where(Book.year == year)

    result = db.execute(stmt.order_by(Book.id))
    books = result.scalars().all()
    return books
