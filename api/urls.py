from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.get_routes ),
    path('projects/', views.get_projects ),
    path('projects/<str:pk>/', views.get_project ),
    path('projects/<str:pk>/vote/', views.review_project ),
    path('projects/tags/remove/', views.remove_tag ),
    
 ]