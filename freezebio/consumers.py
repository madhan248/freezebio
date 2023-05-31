from mqttasgi.consumers import MqttConsumer
from channels.generic.websocket import WebsocketConsumer
import datetime
import threading

import asyncio
import json
from channels.consumer import AsyncConsumer
from random import randint
from time import sleep
from asgiref.sync import sync_to_async


def storetoservicemodel(task,service):
    from api.models import ServiceModel
    return ServiceModel.objects.create(task=task,timestamp=datetime.datetime.now(),service=service)


storeservice = sync_to_async(storetoservicemodel, thread_sensitive=True)



class MyMqttConsumer(MqttConsumer):
    async def connect(self):
        print("connected")
        await self.subscribe('my/testing/topic', 2)

    async def receive(self, mqtt_message):
        from api.models import ServiceModel
        print('Received a message at topic:', mqtt_message['topic'])
        print('With payload', mqtt_message['payload'])
        print('And QOS:', mqtt_message['qos'])
        await storeservice(mqtt_message['topic'],"MQTT")
        # await ServiceModel.objects.create(task=mqtt_message['topic'],timestamp=datetime.datetime.now(),service="MQTT")
        # thread = threading.Thread(group="Mqtt",target=lambda a,b,c:ServiceModel.objects.create(task=a,timestamp=b,service=c),args=(mqtt_message['topic'],datetime.datetime.now(),"MQTT"),name="MQTT")
        # thread.start()
    async def disconnect(self):
        await self.unsubscribe('my/testing/topic')


 

class Calculator(WebsocketConsumer):
    def connect(self):
        self.accept()
  
    def disconnect(self, close_code):
        self.close()   
  
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        expression = text_data_json['expression']
        try:
            result = eval(expression)
        except Exception as e:
            result = "Invalid Expression"
        self.send(text_data=json.dumps({
            'result': result
        }))


class PracticeConsumer(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        self.room_name = None
        self.room_group_name = None
        self.room = None

    async def websocket_connect(self,event):
        try:
            self.room_name = self.scope['url_route']['kwargs']['name']
        except Exception as e:
            print("Exception",e)
        # when websocket connects
        # print("websocket connected",event)
        await self.send({"type":"websocket.accept",})
        # await ServiceModel.objects.create(task=self.room_name,timestamp=datetime.datetime.now(),service="Websocket")
        await storeservice(self.room_name,"Websocket")
        # thread = threading.Thread(group="websocket",target=lambda a,b,c:ServiceModel.objects.create(task=a,timestamp=b,service=c),args=(self.room_name,datetime.datetime.now(),"Websocket"),name="Websocket")
        # thread.start()
        # await self.send({"type":"websocket.send","text":0})
        # await self.send({"type": "websocket.send","text":str(randint(0,100))})

    async def websocket_receive(self,event):
        # when messages is received from websocket
        print("websocket receive",event)
        sleep(1)
        await self.send({"type": "websocket.send","text":self.room_name})

    async def websocket_disconnect(self, event):
        # when websocket disconnects
        print("websocket disconnected", event)
        

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class KafkaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['name']
        self.room_group_name = self.device_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'kafka_message',
                'message': "From Websocket"
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'kafka_message',
                'message': text_data
            }
        )

    # Receive message from room group
    async def kafka_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))




# from channels.generic.websocket import AsyncJsonWebsocketConsumer

# class PracticeConsumer(AsyncJsonWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.room_name = None
#         self.room_group_name = None
#         self.room = None

#     async def connect(self):
#         await self.accept()
#         self.room_name = self.scope['url_route']['kwargs']['pk']
#         await self.send("Connected")

#     async def receive(self, text_data=None, bytes_data=None, **kwargs):
#         if text_data == 'PING':
#             await self.send(self.room_name)


# async def websocket_application(scope, receive, send):
#     while True:
#         event = await receive()

#         if event['type'] == 'websocket.connect':
#             await send({
#                 'type': 'websocket.accept'
#             })

#         if event['type'] == 'websocket.disconnect':
#             break

#         if event['type'] == 'websocket.receive':
#             if event['text'] == 'ping':
#                 await send({
#                     'type': 'websocket.send',
#                     'text': 'pong!'
#                 })