# from api.models import Order, OrderOffer
from asgiref.sync import async_to_sync
import channels.layers
from channels.generic.websocket import (
    JsonWebsocketConsumer,
    WebsocketConsumer,
    AsyncWebsocketConsumer,
)
from django.db.models import signals
from django.dispatch import receiver
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse

# from win10toast import ToastNotifier
from django.contrib.auth.models import User, Group

from channels.auth import AuthMiddleware
from .models import Room


# class OrderOfferConsumer(WebsocketConsumer):
#     def connect(self):

#         self.room_name = self.scope["url_route"]["kwargs"]
#         self.room_group_name = "chat_%s" % self.room_name
#         self.user = self.scope["user"]

#         print(self.user)

#         async_to_sync(self.channel_layer.group_add)(
#             "order_offer_group", self.channel_name
#         )

#         # print(OrderView(Order).content)

#         df = json.loads(OrderView(Order).content)
#         self.accept()

#         self.send(text_data=json.dumps({"payload": df}))
#         # self.send_json(df)

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             "order_offer_group", self.channel_name
#         )
#         self.close()

#     def receive_json(self, content, **kwargs):
#         print(f"Received event: {content}")

#     def events_alarm(self, event):
#         df = json.loads(OrderView(Order).content)
#         self.send(text_data=json.dumps({"payload": df}))
#         print("send")

#     @receiver(signals.post_save, sender=Order)
#     def order_offer_observer(sender, instance, created, **kwargs):
#         layer = channels.layers.get_channel_layer()
#         if not created:
#             async_to_sync(layer.group_send)(
#                 "order_offer_group", {"type": "events.alarm", "payload": {}}
#             )


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        user = self.scope["user"]
        print(user, self.room_group_name, self.room_name)
        await self.accept()
        self.send(text_data=json.dumps({"status": "Whelcome from backend"}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.send(text_data=json.dumps({"status": "disc"}))

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))



def update_or_create_key(dictionary, key, new_element):
    # Check if the key exists in the dictionary
    if key in dictionary:
        # Update the list associated with the existing key, avoiding duplicates
        if new_element not in dictionary[key]:
            dictionary[key].append(new_element)
    else:
        # Create a new key with a list
        dictionary[key] = [new_element]

def remove_element_from_key(dictionary, key, element_to_remove):
    # Check if the key exists in the dictionary
    if key in dictionary:
        # Remove the element from the list associated with the existing key
        if element_to_remove in dictionary[key]:
            dictionary[key].remove(element_to_remove)


user_list = {}
class ChatConsumers(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.username = self.scope["user"].username.title()
        self.group_users = self.scope.get("user").id
        room = Room.add(self.room_name, self.scope.get("user"))
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        # Room.objects.add(self.room_name, self.channel_name, self.scope["user"])

        print( 'username :',self.username)
        print('group_users', self.group_users)
        print('room_name', self.room_name)
        new_list = set(user_list)
        self.accept()
        self.send(text_data=json.dumps({"message":"newuser",  "status": "Whelcome from backend", "userlist": user_list}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        # Access stored information
        message = getattr(self, 'stored_message', None)
        username = getattr(self, 'stored_username', None)
        try:
            remove_element_from_key(user_list, self.room_name, username)
        except:
            pass

        print(f"Disconnected user '{username}' with message '{message}'")

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": 'closed',
                # "username": self.scope["user"].username.title(),
                "username": username,
            },
        )
        
        # Room.objects.remove(self.room_name, self.channel_name)
        # Room.remove_user(self.room_name, self.scope.get("user"))
        self.close()


    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        update_or_create_key(user_list, self.room_name, username)
        # user_list.append(username)
        print(message, username)

        # Store relevant information in the consumer instance
        # self.stored_message = text_data_json.get('message')
        # self.stored_username = text_data_json.get('username')
        self.stored_message = message
        self.stored_username = username

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                # "username": self.scope["user"].username.title(),
                "username": username,
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )
