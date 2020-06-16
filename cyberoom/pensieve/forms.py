# coding=utf-8

from django import forms
from . import models


class PensieveForm(forms.ModelForm):
    class Meta:
        model = models.Pensieve
        fields = '__all__'
