from django.urls import path
from .consumers import PracticeConsumer,KafkaConsumer


websockets_url = [
            path('practice/<name>/',PracticeConsumer.as_asgi()),
            path('kafka/<name>/',KafkaConsumer.as_asgi()),
            ]