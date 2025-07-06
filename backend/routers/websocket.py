from fastapi import WebSocket
from typing import List

live_connections: List[WebSocket] = []

async def send_message_to_clients(message: str):
    for connection in live_connections:
        try:
            await connection.send_text(message)

        except Exception as e:
            print(f"Error sending message to client: {e}")
            live_connections.remove(connection)