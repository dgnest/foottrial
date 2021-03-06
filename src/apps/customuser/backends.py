from apps.customuser.models import MyUser
from django.contrib.auth.models import BaseUserManager


class EmailBackend(object):

    def authenticate(self, **kwargs):
        email = kwargs.get('username')
        password = kwargs.get('password')
        try:
            if email:
                user = MyUser.objects.get(
                    email=BaseUserManager.normalize_email(email)
                )
                if user.check_password(password):
                    return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
