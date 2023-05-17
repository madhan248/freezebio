from django.contrib.auth.backends import ModelBackend,BaseBackend
from django.contrib.auth.models import User
from .models import UserProfile


def authenticate_user(email, password):
    
    try:
        user = UserProfile.objects.get(user__email=email)
        print(user)
    except User.DoesNotExist:
        user = None
    # else:
        # if user.check_password(password):
        #     return user
    return user


class PasswordlessAuthBackend(BaseBackend):
    """Log in to Django without providing a password.

    """
    def authenticate(self,email=None,username=None, **kwargs):
        try:
            return UserProfile.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserProfile.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None