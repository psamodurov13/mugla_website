from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from mugla_site.utils import send
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from .models import Profile
from .tasks import send_email_registration


class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'


def register(request):
    if request.method == 'POST' and 'register-button' in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            send_email_registration.delay(
                user.email,
                'Вы зарегистрированы на сайте',
                f'Спасибо за регистрацию.\n'
                f'Ваш логин: {user.username}\n'
                f'Ваш e-mail: {user.email}\n'
            )
            send_email_registration.delay(
                'psamodurov13@gmail.com',
                'Зарегистрирован новый пользователь',
                f'Зарегистрирован пользователь\n'
                f'Логин: {user.username}\n'
                f'e-mail: {user.email}\n'
            )
            return redirect('profile')
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


def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('home')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ваш профиль успешно обновлен.')
            return redirect('profile', request.user.username)
        else:
            messages.error(request, f'Ваш профиль не обновлен. Проверьте форму')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Редактирование профиля'
    }
    return render(request, 'users/edit_profile.html', context)









