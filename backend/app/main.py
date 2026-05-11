from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import app.modules.models

app = FastAPI()

from app.modules.auth.router import router as auth_router


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "FastAPI funcionando!"}

