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
from .tasks import SignUpTask
import dateutil.parser
from celery import uuid
from celery.task.control import revoke
from django.conf import settings
from datetime import datetime as dtime
import pytz 


#from .tasks import run
# Create your views here.

import pyrebase
config = {
	'apiKey': "AIzaSyD7nDAycSZPQKBYFvlA4KSQj0SebQtm_5c",
    'authDomain': "scheduler-3f833.firebaseapp.com",
    'databaseURL': "https://scheduler-3f833.firebaseio.com",
    'projectId': "scheduler-3f833",
    'storageBucket': "scheduler-3f833.appspot.com",
    'messagingSenderId': "826211709812"
}
firebase = pyrebase.initialize_app(config)
#auth = firebase.auth()
database=firebase.database()

#increment = 1

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
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
        
        print(w)
        
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
       
        post_obj = Post(author=me, title=title, text=text, date_time=date_time,task_id=task_id)
        post_obj.save()
        pk=post_obj.pk
		
        if time_check == 1:
        	SignUpTask.apply_async((pk,),eta=new_time,task_id=task_id)
        if time_check_ten == 1:
            SignUpTask.apply_async((pk,),eta=new_time_ten,task_id=task_id)
     
        post_obj.publish()
        
        
        fire_base ={'user':request.user.email,'title': title, 'text': text, 'date_time': temp }
        
        #node = str(request.user.email) + str(title) + str(temp)
        
        database.child('posts').push(fire_base)
        
        #increment = increment + 1
        
    return redirect('post_list')     
    
@login_required
def post_list(request):
	#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
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
        
            database.child('posts').push(fire_base)          	
            
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'scheduler/post_edit.html', {'form': form})


