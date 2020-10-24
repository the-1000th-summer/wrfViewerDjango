"""_"""

from django.urls import path
from django.conf.urls import url

from app1 import views
from app1.views import tryClass

urlpatterns = [
    path('', views.index),
    path('index/', tryClass.as_view())
]
