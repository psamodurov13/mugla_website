from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'photo', 'content', 'description', 'category', 'tags', 'cities']
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
