from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.profiles, name="profiles"),
    path('users/<str:pk>/', views.user_profile, name="user-profile"),
    path('login-user', views.login_user, name="login"),
    path('register-user', views.register_user, name="register"),
    path('logout-user', views.logout_user, name="logout"),
    path('user-account', views.user_account, name="account"),
    path('edit-account', views.edit_account, name="edit"),
    path('create-skill', views.add_skill, name="create-skill"),
    path('update-skill/<str:pk>/', views.update_skill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.delete_skill, name="delete-skill"),
    path('inbox/', views.inbox, name="inbox"),
    path('messages/<str:pk>/', views.read_message, name="message"),
    path('send-message/<str:pk>/', views.send_message, name="send-message"),
    
  
 ]