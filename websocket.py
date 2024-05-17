from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client
import asyncio
import websockets
import json
import os

app = Flask(__name__)
CORS(app)
client = Client("ShynBui/Vector_db_v3")

# Flask app routes and functions
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    result = client.predict(
        quote=data['quote'],
        history=data['history'],
        api_name="/predict"
    )
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

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
    async for data in websocket:
        data = eval(data)  # Convert string to dictionary (Insecure, use safer methods in production)
        user_id = data.get("user_id")
        friend_id = data.get("friend_id")
        
        message = data.get("message")
        print(f"Received message from user 2 {user_id}: {message} :{friend_id}")
        await register(websocket, user_id)
         # Gửi tin nhắn đến tất cả các client
        for client_user_id, client_socket in clients.items():
            if client_user_id != user_id:
                data = {"user_id": user_id, "message": message, "friend_id":friend_id}
                json_data = json.dumps(data)  # Chuyển đổi từ điển thành chuỗi JSON
                await client_socket.send(json_data)  # Gửi chuỗi JSON
     
    # Sau khi kết thúc kết nối, gọi hàm unregister để xóa kết nối của người dùng
    await unregister(user_id)

async def main():
    # Run Flask app in a separate thread
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, app.run, '0.0.0.0', int(os.environ.get("PORT", 5000)), False)
    # Start WebSocket server
    async with websockets.serve(echo, '', int(os.environ.get("PORT", 5000))):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
