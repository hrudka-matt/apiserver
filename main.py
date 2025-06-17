from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from api.routes import router as books_router
from auth.auth_router import router as auth_router,users_db
from auth.auth_handler import hash_password
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👇 This runs at startup
    username = "user"
    password = "pass"
    if username not in users_db:
        users_db[username] = hash_password(password)
        print(f"✅ Default user '{username}' registered.")
    else:
        print(f"ℹ️ Default user '{username}' already exists.")

    yield  # 🔄 Control passes to the app here

    # 👇 This runs at shutdown (optional)
    print("🚪 App is shutting down...")
    
app = FastAPI(lifespan=lifespan)    
app.include_router(auth_router)
app.include_router(books_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running"}