from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
import uuid

# Create your models here.

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=10, unique=True)
	username = models.CharField(blank=True, null=True, max_length=150)



	REQUIRED_FIELDS = ['username','email']
	USERNAME_FIELD = 'phone_number'
	
	def __init__(self, *args, **kwargs):
		super(CustomUser,self).__init__(*args, **kwargs)
		self._meta.get_field('phone_number').verbose_name = 'Email/Phone Number'

	
	def __str__(self):
		return self.email
		
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    date_time = models.DateTimeField()
    task_id = models.UUIDField(editable=False, default=uuid.uuid4)
    
    #created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
