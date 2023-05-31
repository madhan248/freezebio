
from django.shortcuts import render
from django.db import models
from django.core.management import call_command
# from .serializers import UserProfileSerializer
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.http import HttpResponse
from django.urls import reverse
from rest_framework.views import APIView
from .models import DeviceData,UserProfile,DevicePermission
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json

from freezebio.consumers import PracticeConsumer





def random(request):
    return render(request,'core/home.html',context={'device_list':[{'id':"1","device_id":"madhan"},
        {'id':"2","device_id":"naveen"},{'id':"3","device_id":"kumar"}]})



from django.views.generic import TemplateView
from django.http import HttpResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class LogView(TemplateView):
    template_name = "core/home.html"


# def testview(request):
#     channel_layer = get_channel_layer()

#     async_to_sync(channel_layer.group_send)(
#         'kafka',
#         {
#             'type': 'kafka.message',
#             'message': "msg from test"
#         }
#     )
#     return HttpResponse('<p>Done</p>')

def testview(request):
    print(request.POST.get("msgbox"))
    if request.method == "POST":
        message = request.POST.get("msgbox")
        device_name = request.POST.get("device")
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            device_name,
            {
                'type': 'kafka.message',
                'message': message
            }
        )
        return HttpResponse('<p>Done</p>')
    return render(request,"core/charts.html",{})



# Create your views here.

# def index(request):
#     attrs = {
#         'name': models.CharField(max_length=32),
#         '__module__': 'api.models'
#     }
#     Cars = type("Cars", (models.Model,), attrs)
#     from django.contrib import admin
#     admin.site.register(Cars)
#     # from django.urls import clear_url_caches
#     # clear_url_caches()
#     # call_command('makemigrations')
#     # call_command('migrate')
#     return render(request,"base.html",{})

def index(request):
    if request.user.is_authenticated:
        print("Authenticated User")
        return redirect(reverse("core:home")) 
    return render(request,"core/base.html",{})


@api_view(['GET','POST'])
def example(request):

    return render(request,"core/base.html",{"a":"Apple"})


# @api_view(['GET','POST'])
# def home(request):
#     cursor = connection.cursor()
#     # cursor.execute("INSERT INTO api_animal (name) VALUES ('{0}')".format("Elephant"))
#     cursor.execute("Select * from api_animal")
#     # data = AnimalSerializer(cursor.fetchall()).data
#     # print(cursor.fetchmany())
#     # print(cursor.fetchall())
#     # print(cursor.fetchone())
#     # qs = Animal.objects.all()
#     # qs_json = AnimalSerializer(qs, many=True)
#     # print(qs_json)
#     # return HttpResponse(qs_json, content_type='application/json')
#     json_data =  [{'name':i[1]} for i in cursor.fetchall()]
#     return Response(json_data)

# class DeviceDataView(APIView):

#     def post(self,request):
#         data = request.data
#         data['data'] = json.dumps(data['data'])
#         serializer = DeviceDataSerializer(data=data)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':"Success"})
#         else:
#             # DeviceData(**data).save()
#             # print("success")
#             return Response({"msg":serializer.errors})

    # def get(self,request):
    #     # from datetime import datetime,timedelta
    #     # start = int((datetime.now() - timedelta(days=2)).timestamp())
    #     # data = []
    #     # while start <= int(datetime.now().timestamp()):
    #     #     d = {
    #     #     "device_id":"FBDL00001",
    #     #     "device_type" : "FREEZER",
    #     #     "data": {},
    #     #     "timestamp" : start
    #     #     }
    #     #     # data.append()
    #     #     start = start + 900
    #     #     serializer = DeviceDataSerializer(data=d)
    #     #     print(serializer)
    #     #     if serializer.is_valid():
    #     #         serializer.save()
    #     #         return Response({'msg':"Success"})
    #     #     else:
    #             # return Response({"msg":"Failed"})
    #     # device_data = DeviceData.data_objects.data_query_set("FBDL00001",1681172081,1681341932)
    #     device_data = DeviceData.data_objects.latest_query_set("FBDL00001")
    #     # print(device_data)
    #     serializer = DeviceDataSerializer(device_data)
    #     # if serializer.is_valid():
    #     # return Response(serializer.data)


def user_login(request):
    if request.user.is_authenticated:
        print("Authenticated User")
        return redirect(reverse("home")) 
    if request.method == "POST":
        email = request.POST.get('email')
        user = UserProfile.objects.get(email=email)
        if user.verified:
            login(request,user.user)
            return redirect('home')
        else:
            raise "User not verified, Please Try Again"
    else:
        return render(request,'base.html',{})

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url="login")
def home(request):
    today = datetime.now().date().__str__()
    # try:
        # devices = DevicePermission.objects.select_related('device_config','device_config__device_type').filter(profile__user=request.user)
    # except Exception as e:
        # print(e.__str__())
        # devices = []
    # if devices:
        # devices_list = list(set([i.device_config.device_type for i in devices if i.device_config.display]))
        # context = {"devices":devices,"today":today,"devices_list":devices_list}
    # else:
    # context = {"devices": devices, "today": today}
    # print(context)
    return render(request, 'home.html', {})

def device_filter(request):
    query = request.GET.get('query')
    user = request.user
    try:
        devices = DevicePermission.objects.select_related('device_config','device_config__device_type').filter(profile=user,
                                                                                                               device_config__device_id__icontains=query)
    except Exception as e:
        print("Exception in context.py",e)
        devices = None
    if devices:
        d = {}
        for i in devices:
            if i.device_config.device_type.device_type in d.keys():
                d[i.device_config.device_type.device_type].append({"id":i.device_config.id,"device_name":i.device_config.device_name,
                                                                   "device_id":i.device_config.device_id,"display":i.device_config.display})
            else:
                d[i.device_config.device_type.device_type] = []
                d[i.device_config.device_type.device_type].append({"id":i.device_config.id,"device_name":i.device_config.device_name,
                                                                   "device_id":i.device_config.device_id,"display":i.device_config.display})
        device_list = [{"name":i,"devices":d[i]} for i in d.keys()]
    else:
        device_list = []
    return render(request, 'home.html', {"device_list":device_list})


class UserProfileApi(APIView):

    def get(self,request,*args,**kwargs):
        query = UserProfile.objects.all()
        serializer = UserProfileSerializer(query,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        response = {}
        data = request.data
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['message'] = "data saved successfully"
        else:
            response['message'] = serializer.errors
        return Response(data=response)


# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
# }
