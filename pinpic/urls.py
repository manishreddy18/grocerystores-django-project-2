from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('search/', views.search, name='search'),
    path('logout/', views.logout, name='logout'),
    path('display/<int:pk>', views.display, name='display'),
    path('mostvisited', views.mostvisited, name='mostvisited'),
    path('delete', views.delete, name='delete'),

]
