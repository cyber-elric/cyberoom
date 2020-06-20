# coding=utf-8

from django.shortcuts import redirect, HttpResponseRedirect
from django.views import generic
from . import forms, models
from django.urls import reverse_lazy, reverse


class PensieveList(generic.ListView):
    model = models.Pensieve
    template_name = 'pensieve/list.html'
    context_object_name = 'pensieveList'

    # def get_queryset(self):
    #     return models.Pensieve.objects.all()
    #
    # def get_context_data(self, **kwargs):
    #     context = super(PensieveList, self).get_context_data(**kwargs)
    #     context['pensieve'] = models.Pensieve.objects.all()
    #     return context

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in'):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class PensieveDetail(generic.DetailView):
    model = models.Pensieve
    template_name = 'pensieve/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in'):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class PensieveDelete(generic.DeleteView):
    model = models.Pensieve
    template_name = 'pensieve/delete.html'
    success_url = reverse_lazy('pensieve:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in'):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class PensieveUpdate(generic.UpdateView):
    model = models.Pensieve
    fields = '__all__'
    template_name = 'pensieve/update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in'):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class PensieveCreate(generic.CreateView):
    form_class = forms.PensieveForm
    template_name = 'pensieve/create.html'
    success_url = '/pensieve/'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in'):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
