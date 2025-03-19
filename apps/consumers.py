import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import F

from .models import User, Science


class LeaderBoard(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("leaderboard", self.channel_name)
        print(f"🟢 WebSocket {self.channel_name} 'leaderboard' guruhiga qo‘shildi")

        students = await self.get_sorted_students()
        await self.send(text_data=json.dumps(students))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("students", self.channel_name)

    async def send_students(self):
        students = await self.get_sorted_students()
        await self.channel_layer.group_send(
            "leaderboard",
            {
                "type": "send_student_data",
                "leaderboard": students,
            },
        )

    async def send_student_data(self, event):
        await self.send(text_data=json.dumps(event["leaderboard"]))

    @database_sync_to_async
    def get_sorted_students(self):
        users = User.objects.all().order_by('-gpa')
        return [

            {"place": place,
             "id": user.id,
             "avatar": user.avatar.url,
             "gpa": float(user.gpa) if user.gpa is not None else 0.0,
             "full_name": f'{user.first_name} {user.last_name}',
             "sciences": [{"name": x.name, "percentage": 0, "rank": 1} for x in Science.objects.filter(users__user=user)]
             }
            for place, user in enumerate(users, start=1)
        ]
