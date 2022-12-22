from django.urls import path

from . import views

app_name = 'oauth2jwt'
urlpatterns = [
    path('tookit_auth', views.tookit_auth, name='tookit_auth'),
    path('my_auth', views.my_auth, name='my_auth'),
]