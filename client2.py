import asyncio
import websockets
import json

async def hello(websocket):
    while True:
        message = await websocket.recv()
        print(f"Server sent: {message}")

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await hello(websocket)

if __name__ == "__main__":
    asyncio.run(main())
