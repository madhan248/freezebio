# from rest_framework import serializers
# from .models import UserProfile
# from django.contrib.auth import  authenticate

# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     class Meta:
#     	model = UserProfile
#     	# fields = "__all__"
#     	exclude = ('password',)

#     def create(self, validated_data):
#     	user = super().create(validated_data)
#     	user.set_unusable_password()
#     	user.save()
#     	print(user)
#     	return user

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

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        print("serializers",user)
        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return  



class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")



from rest_framework import serializers, validators


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

# {"email":"madhan@gmail.com","password":"madhan@1"}