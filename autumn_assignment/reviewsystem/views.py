from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
import os
import requests
from django.shortcuts import redirect, render
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.views.generic import TemplateView
from .models import User
from .serializers import UserSerializer
from django.urls import reverse
from dotenv import load_dotenv
load_dotenv()

# DB_NAME = os.getenv("DATABASE_NAME")
# DB_USER =os.getenv("DATABASE_USER")
# DB_PWD = os.getenv("USER_PWD")


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:8000/home'
success_string1 = 'yay'
request_token_url = 'https://channeli.in/open_auth/token/'
request_data_url = 'https://channeli.in/open_auth/get_user_data/'


params = {'client_id': client_id,
        'client_secret': client_secret, 
        'grant_type': 'authorization_code',
        'code': '' ,
        'redirect_uri' : redirect_uri,
        'state': success_string1}

class LoginView(TemplateView):
    template_name = 'reviewsystem/login.html'
    
class HomeView(TemplateView):
    template_name = 'reviewsystem/home.html'


class RequestAccessAPI(APIView):
    def get(self, request):
        print(client_id)
        URL= 'https://channeli.in/oauth/authorise' + "?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&state=" + success_string1
        return redirect(URL)

# class HelloWorldView(APIView):
#     def get(self, request):
#         return HttpResponse("Hello, World!")
    
class CallbackAPI(APIView):
    def get(self, request):
        AUTH_CODE = request.GET.get("code");
        params['code'] = AUTH_CODE
        r = requests.post(request_token_url, data= params)
        response_data = r.json()
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        header = {
                    "Authorization": f"Bearer {access_token}"
                }
        
        r = requests.get(url=request_data_url, headers=header)
        data = r.json()
        print(data)
        enrollment_no = data['username']
        username = data['person']['fullName']
        email = data['contactInformation']['emailAddress']
        date_of_joining = data['student']['startDate']
        phone_no = data['contactInformation']['primaryPhoneNumber']

        users=User.objects.all()
        print(users)

        if User.objects.filter(enrollment_no=enrollment_no).exists():
            print("User exists, logging into user")
            user = User.objects.get(enrollment_no=enrollment_no)
            try:
                login(request=request, user=user)
                print("successfull login for", request.user)
                return redirect("http://localhost:8000/home_page", user)
            except Exception as e:
                return Response("unable to login", e)
        else:
            print("User does not exist, creating new user")

            user=User.objects.create(username=username,enrollment_no=enrollment_no,email=email,date_of_joining=date_of_joining,phone_no=phone_no)
            print(user)
            try:
                login(request, user)
                print("successfull login for", request.user)
                users=User.objects.all()
                print(users)
                return redirect("http://localhost:8000/home_page", user)

            except:
                return Response("unable to login")
             
