from django import forms
from image_cropping import ImageCropWidget, ImageCroppingMixin
from phonenumber_field.formfields import PhoneNumberField

from .models import *


class CreateCompanyForm(ImageCroppingMixin, forms.ModelForm):
    phone = PhoneNumberField()
    whatsapp = PhoneNumberField()
    file_field = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Company

        fields = ['title', 'photo', 'content', 'description', 'type', 'tags', 'cities', 'site', 'phone', 'whatsapp', 'telegram',
                  'note', 'russian_speak', 'english_speak', 'file_field']
        widgets = {
            'title': forms.TextInput(),
            'photo': forms.FileInput(),
            'content': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'type': forms.Select(),
            'tags': forms.SelectMultiple(),
            'cities': forms.SelectMultiple(),
            'site': forms.URLInput(),
            'telegram': forms.TextInput(),
            'note': forms.Textarea(),
            'russian_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'english_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
        self.fields['type'].empty_label = 'Выберите тип организации'
