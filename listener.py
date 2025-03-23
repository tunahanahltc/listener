from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DataModel(BaseModel):
    data: str

@app.get("/")
def read_root():
    return {"message": "FastAPI Çalışıyor 🚀"}

@app.post("/process")
def process_data(data: DataModel):
    return {"processed": data.data.upper()}
