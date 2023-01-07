from django.shortcuts import render,redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout


# Create your views here.
def register(request):
    if request.method == 'POST' and 'register-button' in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Регистрация'})


def user_login(request):
    if request.method == 'POST' and 'login-button' in request.POST:
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form, 'title': 'Вход'})