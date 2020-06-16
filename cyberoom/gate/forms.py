# coding = utf8

from django import forms
from captcha.fields import CaptchaField


class GateForm(forms.Form):
    nameGForm = forms.CharField(label='', max_length=36, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '君名',
        'autofocus': '',
    }))
    passGForm = forms.CharField(label='', max_length=60, widget=forms.PasswordInput(attrs={
        'class': 'textBox',
        'placeholder': '密码',
    }))


class SecureForm(forms.Form):
    nameSForm = forms.CharField(label='', max_length=36, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '君名',
        'autofocus': '',
    }))
    passSForm = forms.CharField(label='', max_length=60, widget=forms.PasswordInput(attrs={
        'class': 'textBox',
        'placeholder': '密码',
    }))
    checkSForm = forms.CharField(label='', max_length=24, widget=forms.TextInput(attrs={
        'class': 'textBox',
        'placeholder': '安全声明',
    }))
    captcha = CaptchaField(label='')
