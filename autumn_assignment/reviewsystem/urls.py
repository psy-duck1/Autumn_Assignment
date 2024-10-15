from django.urls import path

from . import views
urlpatterns = [
    path('login', views.RequestAccessAPI.as_view(), name='login'),
    path('home', views.HelloWorldView.as_view(), name='home'),
]
