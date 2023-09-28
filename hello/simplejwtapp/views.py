from django.shortcuts import render

# Create your views here.
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  #只需修改其序列化器为刚刚自定义的即可