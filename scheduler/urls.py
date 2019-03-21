from django.urls import path
from . import views
#from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
#from django.contrib.auth.views import logout
#from django.contrib.auth import logout

urlpatterns = [
    #path('login', auth_views.login, {'template_name': 'templates/login.html'}, name='login'),
    
    path('login/', LoginView.as_view(template_name='scheduler/login.html'), name="login"),
    path('signup/',views.signup, name='signup'),
    path('', views.post_list, name='post_list'),
    #path('logout/',views.logout, {'next_page': 'login'}, name='logout'),
    path('logout/',views.logout, name='logout'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('new_post/', views.new_post, name='new_post'),
    path('post/', views.post, name='post'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),


    
]
