from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.admin import widgets                                       
from scheduler.models import CustomUser,Post

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=10, min_length=10, help_text='Enter 10 Digit Phone Nummber')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email','phone_number', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': ''})
        
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
