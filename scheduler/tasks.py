#from celery.registry import tasks
from __future__ import absolute_import
from celery.task import Task
from meeting.celery import app
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser,Post
from django.contrib.auth import get_user_model

from pyfcm import FCMNotification
from datetime import datetime
from dateutil import tz
from celery.task import periodic_task
from celery.schedules import crontab
from dateutil.tz import tzlocal
import dateutil.parser
import jwt




@app.task
def SignUpTask(pk=None):
	#initialize()

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
		
	#token = jwt.encode({'email': 'i.mohammedjunaid@gmail.com'},'Pq0AWG4OQv3wWQB4od5Lh8ylAo6oZbMIVQxQSZi2', algorithm='HS256')
	token = user_email.device_id
	
	push_service = FCMNotification(api_key="AAAAwF4OM3Q:APA91bFSAP6H_g5zN6_B99uNtkZQqO8vD4sfQ6Baxnr49P2TFnVDeRuSUvlcsS5VAcFgAcvijMtHxzjbfbLC2SDk89SmiNK7a63aNsBM_e9CJ9ErgU6F2ECzHCZwZgmzQET6HGTru10V")
	registration_id = token

	message_title = temp
	message_body = temp1
	if str(user_email.date_time) > current_utc_time:
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,     message_body=message_body)
		print (result)


@periodic_task(run_every=crontab(minute='*/1'))
def delete_old_posts():

    post = Post.objects.all()
    
    local = tzlocal()
    now = datetime.now()
    now = now.replace(tzinfo = local)
    
    if post:
    	for i in post:
    		z = dateutil.parser.parse(str(i.date_time))
    		print(z)
    		if z < now:
    		    i.delete()
            # log deletion
    return "completed deleting posts at {}".format(now)


	

