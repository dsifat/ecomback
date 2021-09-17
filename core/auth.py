from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()

class LoginSerializer(LoginSerializer):
    pass
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication



class CustomJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_model = get_user_model()



class CoreAuthentication(ModelBackend):

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        if email:
            print(email)
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user