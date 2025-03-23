import asyncio
import websockets

WS_SERVER_URL = "ws://YOUR_RENDER_URL"

async def websocket_client():
    async with websockets.connect(WS_SERVER_URL) as websocket:
        await websocket.send("Merhaba Dünya")

        processed_data = await websocket.recv()
        print(f"İşlenmiş veri alındı: {processed_data}")

asyncio.run(websocket_client())
