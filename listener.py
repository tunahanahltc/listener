from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class DataModel(BaseModel):
    data: str

@app.post("/process")
async def process_data(item: DataModel):
    processed_text = item.data.upper()  # Basit işlem: Büyük harfe çevirme
    return {"processed": processed_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
