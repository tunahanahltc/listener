import os
import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

class DataModel(BaseModel):
    data: str

# Root endpoint - Render kontrol için
@app.get("/")
def read_root():
    return {"message": "FastAPI & WebSocket Çalışıyor 🚀"}

# HTTP API - WebSocket istemcisi buradan POST isteği atacak
@app.post("/process")
def process_data(data: DataModel):
    return {"processed": data.data.upper()}

# WebSocket Bağlantısı
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        processed_data = data.upper()  # WebSocket üzerinden gelen veriyi işleyelim
        await websocket.send_text(f"İşlenmiş veri: {processed_data}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Render’ın verdiği PORT'u kullan
    uvicorn.run(app, host="0.0.0.0", port=port)
