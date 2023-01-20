from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User

from django import forms
from image_cropping import ImageCropWidget, ImageRatioField, ImageCroppingMixin
from .models import *
from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput())
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(ImageCroppingMixin, forms.ModelForm):
    whatsapp = PhoneNumberField()
    hidden = forms.RadioSelect()

    class Meta:
        model = Profile
        fields = ['image', 'cropping_avatar', 'name', 'surname', 'birthday', 'city', 'whatsapp', 'telegram',
                  'instagram', 'hidden']
        widgets = {
            'name': forms.TextInput(),
            'surname': forms.TextInput(),
            'image': ImageCropWidget,
            'birthday': forms.DateInput(attrs={'id': 'datepicker'}),
            # 'cropping_avatar': ImageRatioField,
            'city': forms.Select(),
            'telegram': forms.TextInput(),
            'instagram': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = 'Выберите город'


