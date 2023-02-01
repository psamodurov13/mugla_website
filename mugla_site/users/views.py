from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from blog.models import Post
from mugla_site.utils import send
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.views.generic.detail import DetailView

from .models import Profile
from .tasks import send_email_to_user


class ProfileView(DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(Q(author=User.objects.get(username=self.kwargs['slug']).id) &
                                               Q(is_published=True))
        return context


def register(request):
    if request.method == 'POST' and 'register-button' in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            send_email_to_user.delay(
                user.email,
                'Вы зарегистрированы на сайте',
                f'Спасибо за регистрацию.\n'
                f'Ваш логин: {user.username}\n'
                f'Ваш e-mail: {user.email}\n'
            )
            send_email_to_user.delay(
                'psamodurov13@gmail.com',
                'Зарегистрирован новый пользователь',
                f'Зарегистрирован пользователь\n'
                f'Логин: {user.username}\n'
                f'e-mail: {user.email}\n'
            )
            return redirect('profile', user.username)
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
            return redirect('profile', user.username)
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


class ResetPassword(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'


class ConfirmResetPassword(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'


class DoneResetPasword(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CompleteResetPassword(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class ChangePassword(PasswordChangeView):
    template_name = 'users/password_change_form.html'


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        send_email_to_user.delay(self.request.user.email, 'Пароль изменен', 'Ваш пароль успешно изменен')
        return super().dispatch(*args, **kwargs)













