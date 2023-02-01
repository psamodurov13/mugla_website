from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from django import forms
from image_cropping import ImageCropWidget, ImageCroppingMixin
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox
from crispy_forms.helper import FormHelper
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticOverlayMapWidget

from .models import *


class CreateCompanyForm(ImageCroppingMixin, forms.ModelForm):
    phone = PhoneNumberField()
    whatsapp = PhoneNumberField(help_text='Номер телефона в формате +79001234567 или +905001234567')
    gallery_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # formfield_overrides = {
    #     map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    # }
    # widgets = {
    #     'location': GooglePointFieldWidget,
    # }

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        return helper

    class Meta:
        model = Company
        fields = ['title', 'content', 'description',
                  'location',
                  'type', 'tags', 'cities', 'site', 'phone', 'whatsapp',
                  'telegram', 'note', 'russian_speak', 'english_speak', 'photo', 'gallery_images',
                  'captcha'
                  ]
        widgets = {
            # 'location': GoogleStaticOverlayMapWidget(zoom=12, thumbnail_size='50x50', size='640x640'),
            'title': forms.TextInput(),
            'photo': forms.FileInput(),
            'location': GooglePointFieldWidget(attrs={'class': 'map-widget'}),
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


class AddCompanyPhoto(forms.ModelForm):
    gallery_images = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = CompanyGallery
        fields = ['gallery_images']


class ChangeCompanyForm(forms.ModelForm):

    class Meta:
        model = ChangeCompany
        fields = ['title', 'content', 'description', 'type', 'tags', 'cities', 'site', 'phone', 'whatsapp',
                  'telegram', 'note', 'russian_speak', 'english_speak']

        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'tags': forms.SelectMultiple(),
            'cities': forms.SelectMultiple(),
            'russian_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'english_speak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='changes', verbose_name='Компания')
#     author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='changes', verbose_name='Автор')
#     processed

