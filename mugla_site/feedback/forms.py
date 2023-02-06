from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from .models import *


class FeedbackForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    class Meta:
        model = FeedbackMessage
        fields = ['title', 'category', 'email', 'text']
        widgets = {
            'title': forms.TextInput(),
            'category': forms.Select(),
            'email': forms.EmailInput(),
            'text': forms.Textarea()
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию сообщения'