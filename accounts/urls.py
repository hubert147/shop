from django.contrib import admin
from django.urls import path, include

from shop import views
from accounts import views

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),

]

