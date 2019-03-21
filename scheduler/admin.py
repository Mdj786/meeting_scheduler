from django.contrib import admin
from scheduler.models import CustomUser, Post

admin.site.register(CustomUser)
admin.site.register(Post)

# Register your models here.
