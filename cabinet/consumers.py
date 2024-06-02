import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asyncio import sleep
from random import randint
from channels.layers import get_channel_layer

class DockerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user_name = self.scope['user'].username
        # Создаем уникальную комнату для этого пользователя
        room_name = f"user_{user_name}"
        # Присоединяем пользователя к комнате
        await self.channel_layer.group_add(
            'docker',
            self.channel_name
        )
        print(room_name, user_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("docker", self.channel_name)

    async def container_telemetry(self, event):
        print("hell")
        await self.send_json(event["telemetry"])

    async def container_message(self, event):
        print("hell")
        await self.send_json(event)


class LogsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user_name = self.scope['user'].username
        # Создаем уникальную комнату для этого пользователя
        room_name = f"user_{user_name}"
        # Присоединяем пользователя к комнате
        await self.channel_layer.group_add(
            'docker_logs',
            self.channel_name
        )
        print(room_name, user_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("docker_logs", self.channel_name)

    async def container_logs(self, event):
        await self.send_json(event["logs"])

    async def container_message(self, event):
        await self.send_json(event)