from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
import os
import requests
from django.shortcuts import redirect, render
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout, authenticate
from .models import User
from .serializers import UserSerializer
from django.views.generic import TemplateView
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

class RequestAccessAPI(APIView):
    def get(self, request):
        print(client_id)
        URL= 'https://channeli.in/oauth/authorise' + "?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&state=" + success_string1
        return redirect(URL)

class HelloWorldView(APIView):
    def get(self, request):
        return HttpResponse("Hello, World!")



# class CallbackAPI(APIView):
    
#     def get(self, request):

#         # print("We have the code(user has given permission)")
#         AUTH_CODE = request.GET.get("code")

#         params['code'] = AUTH_CODE

#         r = requests.post(request_token_url, data= params)
#         # print(r.url)
#         # print(r.content)

#         response_data = r.json()
#         access_token = response_data.get('access_token')
#         refresh_token = response_data.get('refresh_token')
#         # print(access_token)
#         # print(refresh_token)

#         # # We have the access token and now will get the user information from it
#         # header = {
#         #             "Authorization": "Bearer "+ access_token,
#         #         }
        
#         # r = requests.get(url=request_data_url, headers=header)
#         # data = r.json()
#         # # roles = data['person']['roles']
#         # # print(roles)

#         # # verifying that the logged in user is from IMG and if yes then adding to our user database is not already
#         # is_member = False
#         # for roles in data['person']['roles']:
#         #     if roles['role'] == 'Maintainer':
#         #         is_member = True
#         #         break
#         # if not is_member:
#         #     return Response("You are not a part of IMG nigga")
        
#         # enrollment_no = data['username']
#         # username = data['person']['fullName']
#         # email = data['contactInformation']['emailAddress']
#         # date_of_joining = data['student']['startDate']
#         # phone_no = data['contactInformation']['primaryPhoneNumber']

#         # users = User.objects.all()
#         # print(users)
#         # # User.objects.all().delete()
#         # # print(users)


#         # if  User.objects.filter(enrollment_no=enrollment_no).exists():
#         #     # means that user already exists
#         #     print("User already exists, so logging in the user")
#         #     user = User.objects.get(enrollment_no=enrollment_no)
#         #     try:
#         #         login(request=request, user=user)
#         #         print("Successful login for ")
#         #         print(request.user)
#         #         return redirect("http://localhost:5173/document")
#         #     except Exception as e:
#         #         return Response("unable to login", e)
#         # else:
#         #     print("User does not exist hence now adding user")

#         #     # this method of creating user can be effectively done using a serializer and then serializer.save() if using modelviewsets
#         #     user = User.objects.create(username= username, email=email, date_of_joining=date_of_joining, phone_no=phone_no, enrollment_no=enrollment_no, tag=enrollment_no)
#         #     print(user)
#         #     try:
#         #         login(request, user)
#         #         print("Successful login for ", request.user)
#         #         users = User.objects.all()
        #         print(users)
        #         print(data)
        #         return redirect("http://localhost:5173/document", user)
        #     except:
        #         return Response("unable to log in")


# class LogoutUser(APIView):
#     def get(self, request):
#         # check if the user is logged in or not 
        
#         if request.user.is_authenticated:
#             logout(request)
#         return Response("Logout was successfull")
    
# class CheckLogin(APIView):
#     def get(self, request):
#         content = {'isLoggedIn': False}
#         if request.user.is_authenticated:
#             print(request.user)
#             serializer = UserSerializer(request.user)
#             content = {'isLoggedIn': True, 'user': serializer.data}
            
#         return Response(content)

# class ClearUserDB(APIView):
#     def get(self, request):
#         User.objects.all().delete()
#         print(User.objects.all())
#         return Response("kardia db clear")