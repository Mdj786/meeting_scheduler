from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import ModelBackend

'''
class MyEmailBackend(object):

    def authenticate(self, username=None, password=None):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(email=username)
            if user.check_password(password):
                return user # return user on valid credentials
            
        except my_user_model.DoesNotExist:
            return None # return None if custom user model does not exist 
        except:
            return None # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
          

class MyEmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)'''
            
class MyEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwars):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None


