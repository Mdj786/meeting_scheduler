from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Post
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import SignUpForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
import datetime
from .tasks import SignUpTask, NotificationTask
import dateutil.parser
from celery import uuid
from celery.task.control import revoke
from django.conf import settings
from datetime import datetime as dtime
import pytz 
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from pyfcm import FCMNotification
import json
import pyrebase


config = {
	'apiKey': "<Your apikey>",
    'authDomain': "<Your authDomain>",
    'databaseURL': "<Your databaseURL>",
    'projectId': "<Your porjectId>",
    'storageBucket': "<Your storageBucket>",
    'messagingSenderId': "<Your messagingSenderId>"
}
firebase = pyrebase.initialize_app(config)
database=firebase.database()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'scheduler/signup.html', {'form': form})
    
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login/')
    
@login_required('')
def post(request):
    time_check = 0
    time_check_ten = 0
    if request.method == 'POST':
        me = request.user
        title = request.POST.get('title', '')
        text  = request.POST.get('text', '')
        
        temp = request.POST.get('date_time', '')
        #usr_title = title
        z = dateutil.parser.parse(temp)
        
        new_date_time = z - datetime.timedelta(minutes=30)
        new_date_time_ten = z - datetime.timedelta(minutes=10)

        local_tz = pytz.timezone ("Asia/Kolkata")

        datetime_without_tz = datetime.datetime.strptime(str(new_date_time), "%Y-%m-%d %H:%M:%S")
        datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None) # No daylight saving time
        datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
        
        datetime_without_tz_ten = datetime.datetime.strptime(str(new_date_time_ten), "%Y-%m-%d %H:%M:%S")
        datetime_with_tz_ten = local_tz.localize(datetime_without_tz_ten, is_dst=None) # No daylight saving time
        datetime_in_utc_ten = datetime_with_tz_ten.astimezone(pytz.utc)
		
		
        current_utc_time = dtime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        w = datetime_in_utc.strftime('%Y-%m-%d %H:%M:%S')
        
        w_ten = datetime_in_utc_ten.strftime('%Y-%m-%d %H:%M:%S')
        
        #print(w)
        
   
        usr_title = title
        
        if w > current_utc_time:
        	time_check = 1
        	
        if w_ten > current_utc_time:
        	time_check_ten = 1
        
        #print(reg_token)
		
        y = w.split(' ')
        
        y_ten = w_ten.split(' ')

        new_time = y[0] + 'T' + y[1]
        new_time_ten = y_ten[0] + 'T' + y_ten[1]
        
        global notif_time, notif_time_ten
        notif_time = new_time
        notif_time_ten = new_time_ten
		
        email = request.user.email
		
        date_time = z
        
        task_id = uuid()
       
        post_obj = Post(author=me, title=title, text=text, date_time=date_time,task_id=task_id)
        post_obj.save()
        pk=post_obj.pk
        
        global t_check, t_check_ten
        t_check = 0
        t_check_ten = 0
		
        if time_check == 1:
        	SignUpTask.apply_async((pk,),eta=new_time,task_id=task_id)
        	t_check = 1
        if time_check_ten == 1:
            SignUpTask.apply_async((pk,),eta=new_time_ten,task_id=task_id)
            t_check_ten = 1
     
        post_obj.publish()
        
        global notif_pk
        notif_pk = pk
        
        
        fire_base ={'user':request.user.email,'title': title, 'text': text, 'date_time': temp }
        database.child(str(pk)).push(fire_base)        
                     
    return redirect('post_list')     
    
@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'scheduler/post_list.html', {'posts' : posts})
	
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'scheduler/post_detail.html', {'post': post})
    
@login_required
def new_post(request):
		return render(request, 'scheduler/new_blog_post.html', {'new_post':new_post})
		
def delete_post(request,pk):
	
	post_obj = get_object_or_404(Post, pk=pk)
	revoke(post_obj.task_id, terminate=True)
	post_obj.delete()
	return redirect('post_list')
		
	
def post_edit(request, pk):
    time_check = 0
    time_check_ten = 0
    post = get_object_or_404(Post, pk=pk)
    revoke(post.task_id)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.date_time = request.POST.get('date_time', '')
            
            temp = request.POST.get('date_time', '')
        
            z = dateutil.parser.parse(temp)
        
            new_date_time = z - datetime.timedelta(minutes=30)
            new_date_time_ten = z - datetime.timedelta(minutes=10)

            local_tz = pytz.timezone ("Asia/Kolkata")

            datetime_without_tz = datetime.datetime.strptime(str(new_date_time), "%Y-%m-%d %H:%M:%S")
            datetime_with_tz = local_tz.localize(datetime_without_tz, is_dst=None) # No daylight saving time
            datetime_in_utc = datetime_with_tz.astimezone(pytz.utc)
            
            datetime_without_tz_ten = datetime.datetime.strptime(str(new_date_time_ten), "%Y-%m-%d %H:%M:%S")
            datetime_with_tz_ten = local_tz.localize(datetime_without_tz_ten, is_dst=None) # No daylight saving time
            datetime_in_utc_ten = datetime_with_tz_ten.astimezone(pytz.utc)

            current_utc_time = dtime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            w = datetime_in_utc.strftime('%Y-%m-%d %H:%M:%S')
            
            w_ten = datetime_in_utc_ten.strftime('%Y-%m-%d %H:%M:%S')
            
            if w > current_utc_time:
        	    time_check = 1
        	
            if w_ten > current_utc_time:
                time_check_ten = 1
		
            y = w.split(' ')
            y_ten = w_ten.split(' ')

            new_time = y[0] + 'T' + y[1]
            new_time_ten = y_ten[0] + 'T' + y_ten[1]
		
            email = request.user.email
		
            date_time = z
        
            task_id = uuid()
            
            post.date_time = z
            
            post.save()
            if time_check == 1:
                SignUpTask.apply_async((pk,),eta=new_time,task_id=task_id)
            if time_check_ten == 1:
        	    SignUpTask.apply_async((pk,),eta=new_time_ten,task_id=task_id)
            
            
            fire_base ={'user':request.user.email,'title': post.title, 'text': post.text, 'date_time': temp }        
            database.child(str(pk)).set(fire_base)          	
            
            return redirect('post_list')
    else:
    
        form = PostForm(instance=post)
    
    
    return render(request, 'scheduler/post_edit.html', {'form': form})

def get_reg_token(request):

	post_obj = Post.objects.get(pk=notif_pk)
	
	x = json.loads(request.body)
	reg_token = x['reg_token']
	post_obj.device_id = reg_token
	
	post_obj.save()
	
	#print(x['reg_token'])
			
	return redirect('post_list')     	
