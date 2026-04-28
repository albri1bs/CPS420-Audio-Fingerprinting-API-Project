from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import views
import subprocess

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register router endpoints that live in views.py
app.include_router(views.router)

@app.get("/")
def root():
    return {"message": "API running"}
