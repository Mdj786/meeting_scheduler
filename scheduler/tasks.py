#from celery.registry import tasks
from __future__ import absolute_import
from celery.task import Task
from meeting.celery import app
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser,Post
from django.contrib.auth import get_user_model


from datetime import datetime
from dateutil import tz



'''
@app.task
def SignUpTask(email=None,tile=None,text=None):
	#print(email)
	from_email = settings.EMAIL_HOST_USER
	#user = User.objects.get(id=user_id) 
	too_email = [email]
	
	temp = "REMINDER"
	
	temp = temp + title
	
	#send_mail('Test Mail','helllo',from_email,too_email,fail_silently=False)
	send_mail(temp,text,from_email,too_email,fail_silently=False)'''

@app.task
def SignUpTask(pk=None):

	from_email = settings.EMAIL_HOST_USER
	
	user_email = Post.objects.get(pk=pk) 

	z = user_email.author.email
	#from_email = ['smps9986@gmail.com']
	too_email = [z]

	temp = "REMINDER: "
	
	temp = temp + user_email.title
	
	
	from_zone = tz.tzutc()
	to_zone = tz.tzlocal()
	
	utc = datetime.strptime(str(user_email.date_time)[:-6], '%Y-%m-%d %H:%M:%S')
	utc = utc.replace(tzinfo=from_zone)
	central = utc.astimezone(to_zone)
	
	temp1 = user_email.text +'\n\n\n'+ "Date and Time: " + str(central)[:-6]
	
	
	current_utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
	
	if str(user_email.date_time) > current_utc_time:
		send_mail(temp,temp1,from_email,too_email,fail_silently=False)
'''	
@app.task
def SignUpTask(user=None):

	from_email = settings.EMAIL_HOST_USER
	
	#user_email = Post.objects.get(pk=pk) 

	z = user[0]
	#from_email = ['smps9986@gmail.com']
	too_email = [z]

	temp = "REMINDER: "
	
	temp = temp + user[1]
	
	#send_mail('Test Mail','helllo',from_email,too_email,fail_silently=False)
	send_mail(temp,user[2],from_email,too_email,fail_silently=False)'''
	

