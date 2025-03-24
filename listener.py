import asyncio
import websockets

WS_SERVER_URL = "wss://ws-cnlo.onrender.com/listener"  # Render'a deploy edince URL'yi güncelle

async def listen():
    async with websockets.connect(WS_SERVER_URL) as websocket:
        print("Connected to WebSocket server as Listener")
        
        while True:
            try:
                message = await websocket.recv()
                print(f"Received from WebSocket: {message}")
                
                # Burada veriyi işleyebilir ve gerekli yanıtı sunucuya gönderebilirsin
                response = f"Processed: {message}"
                await websocket.send(response)
                
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                break

async def main():
    while True:
        try:
            await listen()
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)  # Bağlantı kesilirse 5 saniye sonra tekrar dene

if __name__ == "__main__":
    asyncio.run(main())
