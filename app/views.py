from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from app.models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta
def home(request):
    return render(request,'home.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/chat')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'login.html')
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if not User.objects.filter(username=username):
            User.objects.create_user(username=username,email=email,password=password)
            return redirect('/accounts/login')
        else:
            messages.error(request,'user already exists')
    return render(request,'signup.html')
def signout(request):
    logout(request)
    return redirect('home')


from django.db.models.functions import TruncDate
@login_required
def chat(r):
  response=0
  messages = Chat.objects.filter(user=r.user).annotate(date=TruncDate('time')).values('date').distinct()
  chat_data = {}
  for message in messages:
    print(datetime.today().date())
    
    if message['date']==datetime.today().date():
        date="Today"
    elif message['date']==datetime.today().date()-timedelta(days=1):
        date="Yesterday"
    else:
        date = message['date']
    chat_entries = Chat.objects.filter(user=r.user,time__date=message['date'])
    chat_data[date] = chat_entries
  
  if r.method=="POST":
    msg=r.POST['message']
    response = get_chatbot_response(msg)
    Chat(user=r.user,umsg=msg,cmsg=response,time=datetime.now()).save()
  return render(r,'chat.html',{"chat_data":chat_data})


import json
import os
json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'intents.json')
with open(json_file_path, 'r') as file:
    intents = json.load(file)

import random
def get_chatbot_response(message):
    user_message = message.lower()
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message:
                return random.choice(intent["responses"])
            
    return "I do not understand that."





