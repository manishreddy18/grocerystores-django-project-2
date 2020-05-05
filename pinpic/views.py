from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import StoresList
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
    data = None
    if request.method == 'POST':
            place = request.POST['place']
            api = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyCYKWCly8kboiPaTbMggQJoEgrwQzrDzKg&query=grocery+in+"
            url = api + place
            if not StoresList.objects.filter(place=place).exists():
                req = requests.get(url).json()
                store_names = {}
                for i in range(len(req["results"])):
                    rating = req["results"][i]["rating"]
                    data = StoresList.objects.create(name=req["results"][i]["name"], place=place, count=0, rating=rating)
                    data.save()
            store_names = StoresList.objects.filter(place=place).order_by('-rating')
            return render(request, 'pinpic/storelist.html', {'store_names': store_names})
    else:
        return render(request, 'pinpic/searchbox.html')

def mostvisited(request):
    if request.method == 'POST':
        place = request.POST['place']
        stores = StoresList.objects.filter(place=place,count__gt=0).order_by('-count')[:3]
        return render(request,'pinpic/mostvisited.html',{'store_names':stores})

def logout(request):
    auth.logout(request)
    return redirect('/')

def display(request, pk):
    data = get_object_or_404(StoresList, pk=pk)
    # data = StoresList.objects.get(pk=pk)
    data.count = data.count+1
    data.save()
    return redirect('search')
def delete(request):
    if request.method == 'POST':
        place = request.POST['place']
        StoresList.objects.filter(place=place).delete()
    return redirect('search')