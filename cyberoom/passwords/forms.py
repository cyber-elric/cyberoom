# coding = utf8

from django import forms


class PasswordForm(forms.Form):
    protect = forms.CharField(label='', max_length=120, required=False, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '密保',
        'autofocus': '',
    }))
    app = forms.CharField(label='', max_length=36, required=False, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '用处',
    }))
    length = forms.CharField(label='', max_length=10, required=False, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '长度',
    }))
