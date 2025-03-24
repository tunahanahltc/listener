import asyncio
import websockets
from fastapi import FastAPI, WebSocket
import uvicorn

WS_SERVER_URL = "wss://ws-cnlo.onrender.com/listener"  # Render'a deploy edince URL'yi güncelle

websocket_connection = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global websocket_connection
    asyncio.create_task(connect_to_ws_server())  # WebSocket bağlantısını başlat
    yield
    if websocket_connection:
        await websocket_connection.close()

app = FastAPI(lifespan=lifespan)

async def connect_to_ws_server():
    global websocket_connection
    while True:
        try:
            async with websockets.connect(WS_SERVER_URL) as websocket:
                print("Connected to WebSocket server as Listener")
                websocket_connection = websocket

                while True:
                    message = await websocket.recv()
                    print(f"✅ Listener received from WebSocket: {message}")

                    # Gelen mesajı işleyip yanıt döndür
                    response = f"Processed: {message}"
                    await websocket.send(response)

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed. Reconnecting in 5 seconds...")
            websocket_connection = None
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            websocket_connection = None
            await asyncio.sleep(5)

@app.get("/")
async def root():
    return {"message": "Listener is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected to Listener WebSocket")

    while True:
        try:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")

            if websocket_connection and websocket_connection.open:
                print(f"Forwarding message to WebSocket server: {data}")
                await websocket_connection.send(data)
                response = await websocket_connection.recv()
                print(f"Response from WebSocket server: {response}")
                await websocket.send(response)
            else:
                print("Error: WebSocket server not connected")
                await websocket.send("Error: WebSocket server not connected")

        except Exception as e:
            print(f"WebSocket error: {e}")
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
