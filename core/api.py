# from rest_framework.views import APIView
# from .models import UserProfile
# # from .serializers import UserProfileSerializer,AuthSerializer
# from rest_framework.response import Response


# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

# rest_framework imports
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import  authenticate
from knox.models import AuthToken
# knox imports
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

# local apps import
from core.serializers import UserSerializer, AuthSerializer,LoginUserSerializer

from rest_framework.authentication import SessionAuthentication



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



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
    	data = request.data 
    	user = authenticate_user(data['email'],data['password'])
    	if user:
    		return Response({
	            "user": UserSerializer(user, context=self.get_serializer_context()).data,
	            "token": AuthToken.objects.create(user)[1]
	            })
    	else:
    		return Response({"message":"error"})
