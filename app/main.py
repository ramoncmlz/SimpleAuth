from fastapi import FastAPI
from app.api.endpoints import router
from app.storage.db import init_db

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"status": "ok"}
