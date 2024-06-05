from flask import Flask, jsonify
from flask_cors import CORS
import asyncio
import websockets
import json
import os

app = Flask(__name__)
CORS(app)

# WebSocket server functions
clients = {}

async def register(websocket, user_id):
    # Lưu kết nối của người dùng dựa trên user_id
    clients[user_id] = websocket

async def unregister(user_id):
    # Xóa kết nối của người dùng dựa trên user_id
    if user_id in clients:
        del clients[user_id]

async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)  # Sử dụng json.loads để chuyển đổi chuỗi JSON thành từ điển
        user_id = data.get("user_id")
        friend_id = data.get("friend_id")

        print(f"Received message from user {user_id}: {data['message']} to friend {friend_id}")
        await register(websocket, user_id)
        # Gửi tin nhắn đến bạn bè của người dùng
        if friend_id in clients:
            await clients[friend_id].send(json.dumps(data))  # Gửi chuỗi JSON

    # Sau khi kết thúc kết nối, gọi hàm unregister để xóa kết nối của người dùng
    await unregister(user_id)

async def main():
    port = int(os.environ.get("PORT", "8000"))  # Đặt giá trị mặc định cho PORT nếu không được định nghĩa trong biến môi trường
    async with websockets.serve(echo, host='', port=port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
