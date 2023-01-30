from crispy_forms.helper import FormHelper
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
from .models import *


class PostCommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return helper

    class Meta:
        model = PostComments
        fields = ('content', 'captcha')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class CompanyCommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return helper

    class Meta:
        model = CompanyComments
        fields = ('content', 'captcha')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
