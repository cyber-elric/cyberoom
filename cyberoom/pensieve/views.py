# coding=utf-8

from django.shortcuts import render
from django.views import generic
from . import forms, models
from django.urls import reverse_lazy


class PensieveList(generic.ListView):
    model = models.Pensieve
    template_name = 'list.html'
    context_object_name = 'pensieveList'

    def get_queryset(self):
        return models.Pensieve.objects.all()


class PensieveDetail(generic.DetailView):
    model = models.Pensieve
    template_name = 'detail.html'


class PensieveDelete(generic.DeleteView):
    model = models.Pensieve
    template_name = 'delete.html'
    success_url = reverse_lazy('pensieve:list')


class PensieveUpdate(generic.UpdateView):
    model = models.Pensieve
    fields = '__all__'
    template_name = 'update.html'


class PensieveCreate(generic.CreateView):
    form_class = forms.PensieveForm
    template_name = 'create.html'
    success_url = '/pensieve/'

    def form_invalid(self, form):
        return render(None, '404.html')
