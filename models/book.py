from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict

@dataclass
class Book:
    id: int = None
    title: str = ""
    price: str = ""

class BookRequest(BaseModel):
    title: str
    price: str

class BookResponse(BaseModel):
    id: int
    title: str
    price: str

    model_config = ConfigDict(from_attributes=True)
