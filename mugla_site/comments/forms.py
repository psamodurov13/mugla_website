from django import forms

from .models import *


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = PostComments
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class CompanyCommentForm(forms.ModelForm):

    class Meta:
        model = CompanyComments
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }