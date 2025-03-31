from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
from uuid import uuid4
from sqlalchemy.orm import Session
from src.helpers.jwt_config import jwt_config
from src.db.db_mysql import databaseMysql
from src.dao.grupos_sanguineos_dao import grupos_sanguineos_dao
import jwt
import asyncio

class WebSocketManager:
    """
    Clase para manejar conexiones WebSocket con soporte de canales.
    """
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.channels: Dict[str, set] = {}
        self.chat_rooms: Dict[str, list[str]] = {}
        self.user_client_map: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, token: str):
        try:
            payload = jwt_config.valida_token(token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            await websocket.close(code=1008)
            return None, []

        client_id = str(uuid4())
        self.clients[client_id] = websocket
        
        user_id = payload.get("id")
        self.user_client_map[user_id] = client_id 

        roles = payload.get("roles", [])
        for role in roles:
            if role not in self.channels:
                self.channels[role] = set()
            self.channels[role].add(client_id)

        await websocket.accept()
        await websocket.send_json({
            "client_id": client_id,
            "roles_asigned": roles,
            "message": f"Conectado a roles/canales: {roles}"
        })

        return client_id, roles

    async def listen(self, websocket: WebSocket, client_id: str, roles: list):
        try:
            while True:
                data = await websocket.receive_json()
                to_client = data.get("to")
                message = data.get("message")
                print(data)
                print(to_client)
                print(message)

                # Asocia al paciente al doctor si no está
                for role in roles:
                    if "Paciente" in role and to_client:
                        self.add_to_chat_room(to_client, client_id)

                # Envía el mensaje privado
                await self.send_private_message(client_id, to_client, message)
        except WebSocketDisconnect:
            self.disconnect(client_id, roles)


    def disconnect(self, client_id: str, roles: list):
        for role in roles:
            if role in self.channels:
                self.channels[role].discard(client_id)
        self.clients.pop(client_id, None)

    async def broadcast(self, data: dict, channels: list[str]):
        """
        Envía un mensaje a todos los clientes pertenecientes a uno o más canales (roles).

        Args:
            data (dict): Datos a enviar.
            channels (list): Lista de nombres de canales (roles).
        """
        # Usamos un set para evitar enviar dos veces a un mismo cliente
        unique_clients = set()
        for channel in channels:
            if channel in self.channels:
                unique_clients.update(self.channels[channel])

        disconnected = []
        for client_id in unique_clients:
            client = self.clients.get(client_id)
            if client:
                try:
                    await client.send_json(data)
                except Exception:
                    disconnected.append(client_id)

        for client_id in disconnected:
            # Se eliminan de todos los canales en los que estén
            self.disconnect(client_id, channels)

    async def send_message_to_client(self, client_id: str, data: dict):
        client = self.clients.get(client_id)
        if client:
            await client.send_json(data)
            
    def broadcast_sync(self, data: dict, channels: list[str]):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(self.broadcast(data, channels))
        else:
            loop.run_until_complete(self.broadcast(data, channels))
            
    async def send_private_message(self, sender_id: str, receiver_id: str, message: str):
        """Enviar mensaje privado entre cliente y cliente."""
        receiver_ws = self.clients.get(receiver_id)
        if receiver_ws:
            await receiver_ws.send_json({
                "from": sender_id,
                "message": message
            })
            
    def add_to_chat_room(self, doctor_id: str, patient_id: str):
        """Asocia un paciente a un doctor cuando inicia el chat."""
        if doctor_id not in self.chat_rooms:
            self.chat_rooms[doctor_id] = []
        if patient_id not in self.chat_rooms[doctor_id]:
            self.chat_rooms[doctor_id].append(patient_id)
            
    def send_message_to_client_sync(self, client_id: str, data: dict):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(self.send_message_to_client(client_id, data))
        else:
            loop.run_until_complete(self.send_message_to_client(client_id, data))


# Instancia global para usar en otros módulos
ws_manager = WebSocketManager()
