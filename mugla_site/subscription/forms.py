from django import forms
from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e-mail'})
        }

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['email'].label = ""
