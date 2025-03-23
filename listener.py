import os
import asyncio
import uvicorn
import requests  # FastAPI'ye istek atmak için
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import websockets

app = FastAPI()

class DataModel(BaseModel):
    data: str

# Root endpoint (Render için)
@app.get("/")
def read_root():
    return {"message": "FastAPI & WebSocket Çalışıyor 🚀"}

# HTTP API - WebSocket buraya istek atacak
@app.post("/process")
def process_data(data: DataModel):
    return {"processed": data.data.upper()}

# WebSocket Bağlantısı - ws_server.js'e bağlanmak için
async def listen_to_ws_server():
    WS_SERVER_URL = "wss://ws-cnlo.onrender.com"  # ws_server.js'in URL'si
    async with websockets.connect(WS_SERVER_URL) as websocket:
        while True:
            data = await websocket.recv()
            print(f"İstemciden gelen mesaj: {data}")

            # FastAPI'ye istek at
            try:
                FASTAPI_URL = "http://0.0.0.0:10000/process"  # FastAPI servisi
                response = requests.post(FASTAPI_URL, json={"data": data})
                processed_data = response.json().get("processed", "Hata")
            except Exception as e:
                processed_data = f"Hata: {str(e)}"

            # WebSocket üzerinden gelen veriyi işlem sonrasında geri gönder
            await websocket.send(f"İşlenmiş veri: {processed_data}")

# FastAPI'nin WebSocket endpoint'i
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"İstemciden gelen mesaj: {data}")
        await websocket.send_text(f"Veri alındı: {data}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  
    uvicorn.run(app, host="0.0.0.0", port=port)

    # ws_server.js'i dinlemeye başla
    asyncio.run(listen_to_ws_server())  # WebSocket bağlantısını başlat
