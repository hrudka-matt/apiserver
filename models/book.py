from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict

@dataclass
class Book:
    id: int = None
    title: str = ""
    price: str = ""
    ref: str = ""

class BookRequest(BaseModel):
    title: str
    price: str
    ref: str

class BookResponse(BaseModel):
    id: int
    title: str
    price: str
    ref: str

    model_config = ConfigDict(from_attributes=True)
