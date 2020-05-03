from django.shortcuts import render , redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import requests
# Create your views here.

def home(request):
    return render(request, 'pinpic/home.html')

def register(request):
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'UserName Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'PassWord not Matching')
            return redirect('register')

    else:
        return render(request,'pinpic/register.html')

def login(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = user_name,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('search')
        else:
            messages.info(request, 'Invalid Credentials!!!')
            return redirect('login')
    else:
        return render(request, 'pinpic/login.html')

def search(request):
    if request.method == 'POST':
            place = request.POST['place']
            api = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyCYKWCly8kboiPaTbMggQJoEgrwQzrDzKg&query=grocery+in+"
            url = api + place
            req = requests.get(url).json()
            store_names = {}
            for i in range(len(req["results"])):
                store_names[req["results"][i]["name"]]= req["results"][i]["rating"]
            return render(request, 'pinpic/searchbox.html', {'store_names': store_names})
    else:
        return render(request, 'pinpic/searchbox.html')


def logout(request):
    auth.logout(request)
    return redirect('/')