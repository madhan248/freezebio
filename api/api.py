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
from .authentication import authenticate_user
from rest_framework.decorators import action
# local apps import
from .serializers import UserSerializer,LoginUserSerializer,CreateUserProfileSerializer,UserProfileSerializer

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

    def post(self, request, *args, **kwargs):
        data = request.data
        user = authenticate_user(data.get('email'),data.get('password'))
        if user:
            userdata = CreateUserProfileSerializer(user).data
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
    serializer_class = CreateUserProfileSerializer
    # permission_classes = [permissions.IsAuthenticated, ]
    # def get(self,request,*args,**kwargs):
    #     return Response(ProfileSerializer(UserProfile.objects.all(),many=True).data)

    def post(self,request,*args,**kwargs):
        response = {}
        data = request.data
        try:
            user_exists = UserProfile.objects.get(user__email=data['user'].get('email'))
        except:
            user_exists = None
        if not user_exists:
            serializer = CreateUserProfileSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response['message'] = "User Registered Successfully"
            else:
                response['message'] = serializer.errors
        else:
            response['message'] = "User Already Registered Please SignIn"
        return Response(response)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=True, methods=['post','get'])
    def some_action(self, request, pk=None):
        return Response({"message":"Some Actions","pk":pk,"ports":request.get_port()})