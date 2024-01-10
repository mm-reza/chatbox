from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
User = get_user_model()
# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=150, unique=True)
    users = models.ManyToManyField(get_user_model(), related_name="rooms")

    @classmethod
    @sync_to_async
    def add(cls, room_name, user):
        room, created = cls.objects.get_or_create(room_name=room_name)
        room.users.add(User)
        return created  # sockets => join or create

    @classmethod
    @sync_to_async
    def users_count(cls, room_name):
        rooms = cls.objects.filter(room_name=room_name)
        if rooms.exists():
            return rooms.first().users.count()
        return 0