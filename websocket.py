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
    clients[user_id] = websocket

async def unregister(user_id):
    if user_id in clients:
        del clients[user_id]

async def echo(websocket, path):
    async for data in websocket:
        data = json.loads(data)  # Use json.loads for security
        user_id = data.get("user_id")
        friend_id = data.get("friend_id")
        message = data.get("message")
        await register(websocket, user_id)
        for client_user_id, client_socket in clients.items():
            if client_user_id != user_id:
                data = {"user_id": user_id, "message": message, "friend_id": friend_id}
                json_data = json.dumps(data)
                await client_socket.send(json_data)
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
