from django import forms
from .models import *


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = PostComments
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }