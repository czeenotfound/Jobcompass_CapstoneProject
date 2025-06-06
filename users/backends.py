from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):  # Use CamelCase
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Authenticate by either username or email
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # To avoid timing attacks
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            # In case multiple users are found, get the first one
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
