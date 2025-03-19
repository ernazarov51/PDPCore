from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import ImageField, DecimalField, Model, CharField, ForeignKey, CASCADE, SmallIntegerField


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions_set")

    avatar = ImageField(upload_to='user/avatar')
    gpa = DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.broadcast_leaderboard_update()

    def broadcast_leaderboard_update(self):
        channel_layer = get_channel_layer()
        users = User.objects.all().order_by('-gpa')
        students_data = [
            {"place": place,
             "id": user.id,
             "avatar": user.avatar.url if user.avatar else None,
             "gpa": float(user.gpa),
             "full_name": f'{user.first_name} {user.last_name}',
             }
            for place, user in enumerate(users, start=1)
        ]
        async_to_sync(channel_layer.group_send)(
            "leaderboard",
            {
                "type": "send_student_data",
                "leaderboard": students_data
            }
        )

    def __str__(self):
        return self.username


class Science(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(Model):
    science = ForeignKey('apps.Science', on_delete=CASCADE, related_name='tasks')
    title = CharField(max_length=255)
    total = SmallIntegerField(default=0)

    def __str__(self):
        return self.title


class TaskResult(Model):
    task = ForeignKey('apps.Task', on_delete=CASCADE, related_name='results')
    user_earned = SmallIntegerField(default=0)
    user=ForeignKey(User, on_delete=CASCADE, related_name='results')

    def __str__(self):
        return self.task.title


class UserScience(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='sciences')
    science = ForeignKey('apps.Science', on_delete=CASCADE, related_name='users')

    def __str__(self):
        return self.user.username + ' ' + self.science.name

