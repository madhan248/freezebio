# from rest_framework.views import APIView
# from .models import UserProfile
# # from .serializers import UserProfileSerializer,AuthSerializer
# from rest_framework.response import Response


# from rest_framework.permissions import IsAuthenticated

# from rest_framework.views import APIView

# from knox.auth import TokenAuthentication
# from knox.views import LoginView as KnoxLoginView


# from django.contrib.auth import login

# # rest_framework imports
# from rest_framework import generics, authentication, permissions
# from rest_framework.settings import api_settings
# from rest_framework.authtoken.serializers import AuthTokenSerializer

from .authentication import authenticate_user



# class ExampleView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         content = {
#             'foo': 'bar'
#         }
#         return Response(content)


# class LoginView(KnoxLoginView):
#     # login view extending KnoxLoginView
#     serializer_class = AuthSerializer
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         # serializer = AuthTokenSerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # user = serializer.validated_data['email']
#         # login(request, user)
#         print(request)
#         return super(LoginView, self).post(request, format=None) 



# class LoginApiView(APIView):

# 	def get(self,request,*args,**kwargs):
# 		email = request.query_params.get('email',None)
# 		try:
# 			profile = UserProfile.objects.get(email=email)
# 			serializer = UserProfileSerializer(profile)
# 			return Response(data=serializer.data)
# 		except Exception as e:
# 			print(e)
# 			return Response({})

# 	def post(self,request,*args,**kwargs):
# 		print(request.data)
# 		serializer = UserProfileSerializer(request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response({"message":"Data Stored Successfully"})
# 		else:
# 			return Response(serializer.errors)





# django imports
from django.contrib.auth import login
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import  authenticate
from knox.models import AuthToken
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import viewsets

# local apps import
from .serializers import UserSerializer,ProfileSerializer,LoginUserSerializer

from rest_framework.authentication import SessionAuthentication
from .models import UserProfile



class CreateUserView(generics.CreateAPIView):
    # Create user API view
    serializer_class = UserSerializer


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
    	data = request.data
    	email = data['email']
    	password = data['password']
    	# serializer = AuthTokenSerializer(data=request.data)
    	user = authenticate(email=email,password=password)
    	print(user,email,password)
    	if user:
    		print("Authenticated")
    	serializer = AuthSerializer(data=request.data)
    	serializer.is_valid(raise_exception=True)
    	user = serializer.validated_data['email']
    	login(request, user)
    	return super(LoginView, self).post(request, format=None)    


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user



class LoginAPI(APIView):
    serializer_class = LoginUserSerializer

    def get(self,request):
        from django.contrib.auth.models import User
        user = request.user
        d = {"user":user.username}
        if user:
            try:
                profile = User.objects.get(username=user.username)
            except Exception as e:
                d['data'] = e.__str__()
            else:
                d["data"] = profile.users.designation
            finally:
                d['dataf'] = "Finally Block"
        return Response(d)

    def post(self, request, *args, **kwargs):
        # from django.contrib.sessions.models import Session
        # sessions = Session.objects.all()
        # print(sessions)
        
        data = request.data
        user = authenticate_user(data.get('email'),data.get('password'))
        if user:
            userdata = ProfileSerializer(user).data
            userdata['token'] = AuthToken.objects.create(user.user)[1]
            userdata['email'] = data.get('email')
            return Response(userdata)
        else:
            return Response({"message":"error"})

class LogoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.get('token_key')
        print(request.data.get('token_key')[:8])
        if user:
            token = AuthToken.objects.get(token_key=data)
            return Response({"message":token.user.username,"data":data})
        else:
            return Response({"message":"error"})

class NewView(APIView):

    def get(self,request,*args,**kwargs):
        return Response({'message':f"Get API{pk}"})

class CreateUserAPI(APIView):
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated, ]
    # def get(self,request,*args,**kwargs):
    #     return Response(ProfileSerializer(UserProfile.objects.all(),many=True).data)

    def post(self,request,*args,**kwargs):
        response = {}
        data = request.data
        data['user']['username'] = data['user']['email'].split('@')[0]
        user_serializer = UserSerializer(data=data['user'])
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            data['user'] = user_serializer.data['id']
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['message'] = "data saved"
            else:
                response['message'] = serializer.errors
        return Response(response)