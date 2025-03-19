from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import User


@receiver(post_save, sender=User)
def student_updated(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    users = User.objects.all().order_by('-gpa')
    # Convert User objects to a list of dictionaries
    students_data = [
            {"place": place,
             "id": user.id,
             "avatar": user.avatar.url,
             "gpa":float(user.gpa),
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