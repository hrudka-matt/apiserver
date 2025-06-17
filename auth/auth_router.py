from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth.auth_handler import hash_password, verify_password, create_access_token
from typing import Dict

router = APIRouter()
users_db: Dict[str, str] = {}  # username: hashed_password (for demo purposes)

class RegisterModel(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: RegisterModel):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.username] = hash_password(user.password)
    return {"msg": "User registered"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username not in users_db or not verify_password(password, users_db[username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": username})
    print(token); 
    return {"access_token": token, "token_type": "bearer"}
