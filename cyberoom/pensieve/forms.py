# coding=utf-8

from django import forms
from . import models


class PensieveForm(forms.ModelForm):
    class Meta:
        model = models.Pensieve
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'titleTextBox',
                'placeholder': 'Title',
                'autofocus': '',
            }),

            'content': forms.Textarea(attrs={
                'class': 'contentTextBox',
                'placeholder': 'Content',
            }),

            'up': forms.TextInput(attrs={
                'type': 'hidden',
            }),
        }
