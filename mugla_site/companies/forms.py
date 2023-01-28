from django import forms
from image_cropping import ImageCropWidget, ImageCroppingMixin
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper

from .models import *


class CreateCompanyForm(ImageCroppingMixin, forms.ModelForm):
    phone = PhoneNumberField()
    whatsapp = PhoneNumberField(help_text='Номер телефона в формате +79001234567 или +905001234567')
    gallery_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return helper

    class Meta:
        model = Company

        fields = ['title', 'content', 'description', 'type', 'tags', 'cities', 'site', 'phone', 'whatsapp',
                  'telegram', 'note', 'russian_speak', 'english_speak', 'photo', 'gallery_images',
                  'captcha'
                  ]
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


class GalleryForm(forms.ModelForm):
    gallery_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    photo = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = CompanyGallery
        fields = ['gallery_images']
