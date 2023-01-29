from django import forms
from .models import *
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper


class CreatePostForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return helper

    class Meta:
        model = Post
        fields = ['title', 'photo', 'content', 'description', 'category', 'tags', 'cities', 'captcha']
        widgets = {
            'title': forms.TextInput(),
            'photo': forms.FileInput(),
            'content': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'category': forms.Select(),
            'tags': forms.SelectMultiple(),
            'cities': forms.SelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'
