import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asyncio import sleep
from random import randint

class DockerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("docker", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("docker", self.channel_name)

    async def container_telemetry(self, event):
        print("hell")
        await self.send_json(telemetry_data=event["telemetry"])

    async def container_message(self, event):
        await self.send_json(event)
