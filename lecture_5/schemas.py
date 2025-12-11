from pydantic import BaseModel,Field
from typing import Optional

class BookCreate(BaseModel):
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=100)
    year: int = Field(..., ge=0, le=2100)


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
