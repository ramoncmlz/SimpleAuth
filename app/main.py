from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok"}
