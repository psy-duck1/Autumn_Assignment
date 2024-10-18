from django.urls import path

from . import views
urlpatterns = [
    path('login', views.RequestAccessAPI.as_view(), name='login'),
    path('home', views.CallbackAPI.as_view(), name='home'),
    path('', views.LoginView.as_view(), name='login_page'),
    path('home_page', views.HomeView.as_view(), name='home_page'),

]
