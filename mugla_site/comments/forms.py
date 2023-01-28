from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from .models import *


class PostCommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    class Meta:
        model = PostComments
        fields = ('content', 'captcha')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class CompanyCommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    class Meta:
        model = CompanyComments
        fields = ('content', 'captcha')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
