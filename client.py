import asyncio
import websockets
import json  # Import thư viện json để chuyển đổi từ điển thành chuỗi JSON

async def send_message(uri, user_id, message, friend_id):
    async with websockets.connect(uri) as websocket:
        # t = await websocket.recv()
        data = {"user_id": user_id, "message": message, "friend_id":friend_id}
        json_data = json.dumps(data)  # Chuyển đổi từ điển thành chuỗi JSON
        await websocket.send(json_data)  # Gửi chuỗi JSON
        print(f"> Gửi: {json_data}")
  

async def main():
    uri = "ws://localhost:8765"
    user_id = input("Enter user ID: ")
    friend_id = input("Enter user ID: ")

    while True:
     
        message = input("Enter message to send: ")
        await send_message(uri, user_id, message ,friend_id)
     
if __name__ == "__main__":
    asyncio.run(main())
