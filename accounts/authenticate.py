from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class PhoneNumberAuthenticateBacked(BaseBackend):
    def authenticate(self, request, phone_number=None):
        try:
            print(phone_number)
            user = User.objects.get(phone_number=phone_number)
            print('user:', user)
            return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
