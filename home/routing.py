import django
django.setup()

from django.urls import re_path, path
from django.urls import re_path as url


from django.core.asgi import get_asgi_application

from . import consumers

#    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),


websocket_urlpatterns = [
    # path('ws/user/', consumers.OrderOfferConsumer),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumers.as_asgi()),
]
