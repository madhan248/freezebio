# from rest_framework import serializers,validators
# from .models import UserProfile
# from django.contrib.auth import  authenticate

# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     class Meta:
#     	model = UserProfile
#     	# fields = "__all__"
#     	exclude = ('password',)



# class AuthSerializer(serializers.Serializer):
#     '''serializer for the user authentication object'''
#     email = serializers.EmailField()
#     # password = serializers.CharField(
#     #     style={'input_type': 'password'},
#     #     trim_whitespace=False
#     # )    
#     def validate(self, attrs):
#     	print("attrs",attrs)
#     	email = attrs.get('email')
#     	# password = attrs.get('password')
#     	user = authenticate(request=self.context.get('request'),email=email)
#     	if not user:
#     		msg = ('Unable to authenticate with provided credentials')
#     		raise serializers.ValidationError(msg, code='authentication')
#     	attrs['user'] = user
#     	return

from django.contrib.auth.models import User
from django.contrib.auth import  authenticate
from .models import UserProfile,Events
from rest_framework import serializers
from django.contrib.auth import get_user_model

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # fields = '__all__'
        fields = ("id","username", "email", "first_name", "last_name")
        # write_only_fields = ('password')
        # extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data) 

#     Create User Without Password
#     def create(self, validated_data):
#       user = super().create(validated_data)
#       user.set_unusable_password()
#       user.save()
#       print(user)
#       return user

class ProfileSerializer(serializers.ModelSerializer):
    # email = serializers.SerializerMethodField('get_email')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')
    class Meta:
        model = UserProfile
        fields = ('number','organization','verified','admin','Dob','designation','email','username')
        depth = 1
    # Get Email from user model
    def get_email(self,userprofile):
        return userprofile.user.email

# {"email":"madhan@gmail.com","password":"madhan@1"}