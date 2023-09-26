from django.urls import path
from rest_framework import routers

from . import views

app_name = 'oauth2jwt'
urlpatterns = [
    path('test_auth', views.test_auth, name='test_auth'),
    path('my_auth', views.my_auth, name='my_auth'),
]