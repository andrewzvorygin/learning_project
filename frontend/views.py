from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user_profile.models import MainCycle
import re


def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        main_cycle = MainCycle.objects.filter(user=request.user)[0]
        return render(request, 'index.html', {'user': user[0], 'mainCycle': main_cycle})
    else:
        return redirect('login')


def user_login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'invalid': True})
    else:
        return render(request, 'login.html', {'invalid': False})


def user_logout(request):
    logout(request)
    return redirect('login')


def name_invalid_password(password):
    if 6 > len(password):
        return 'invalid_password_len'
    if len(re.findall(r'[a-z]', password)) == 0:
        return 'invalid_password_lowercase'
    if len(re.findall(r'[A-Z]', password)) == 0:
        return 'invalid_password_uppercase'
    if len(re.findall(r'[0-9]', password)) == 0:
        return 'invalid_password_number'


def user_registration(request):
    if request.method == "POST":
        username = request.POST["username"]
        existing_user = User.objects.filter(username=username)
        if len(existing_user) == 0:
            password = request.POST["password"]
            name_invalid = name_invalid_password(password)
            if name_invalid is not None:
                return render(request, 'registration.html', {name_invalid: True})
            user = User.objects.create_user(username, '', password)
            user.save()
            main_cycle = MainCycle()
            main_cycle.user = user
            main_cycle.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return render(request, 'index.html', {'user': user})
        else:
            return render(request, 'registration.html', {'invalid': True})
    else:
        return render(request, 'registration.html', {'invalid': False})
