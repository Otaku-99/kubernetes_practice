from fastapi import FastAPI
from app import add

app = FastAPI(title="CI Demo API")


@app.get("/")
def home():
    return {"message": "Application running on Kubernetes"}


@app.get("/add")
def calculate_addition(a: int, b: int):
    return {"result": add(a, b)}


@app.get("/health")
def health():
    return {"status": "healthy"}