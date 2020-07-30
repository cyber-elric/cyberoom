# coding=utf-8

from django.shortcuts import redirect, HttpResponseRedirect
from django.views import generic
from . import forms, models
from django.urls import reverse_lazy, reverse


# 
class PensieveList(generic.ListView):
    # model = models.Pensieve
    template_name = 'pensieve/list.html'
    context_object_name = 'pensieveList'

    # 检查登录状态，未登录则返回登录界面
    def dispatch(self, request, *args, **kwargs):   
        if not request.session.get('checked_in', None):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    # 只展示用户自己的pensieve
    def get_queryset(self):
        return models.Pensieve.objects.filter(up=self.request.session.get('up', None))


class PensieveDetail(generic.DetailView):
    template_name = 'pensieve/detail.html'
    queryset = models.Pensieve.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in', None):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    # 用户只能查看自己的pensieve
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.up != self.request.session.get('up', None):
            raise Http404()
        return obj


class PensieveCreate(generic.CreateView):
    form_class = forms.PensieveForm
    template_name = 'pensieve/create.html'
    success_url = '/pensieve/'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in', None):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    # 自动为用户处理pensieve的拥有者
    def get_initial(self):
        initial = super(PensieveCreate, self).get_initial()
        initial['up'] = self.request.session.get('up', None)
        return initial

    
    # def get_context_data(self, **kwargs):
    #     context = super(PensieveUpdate, self).get_context_data(**kwargs)
    #     context['uper'] = forms.PensieveForm(initial={
    #         'up': self.request.session.get('up', None),
    #     })
    #     return context


class PensieveUpdate(generic.UpdateView):
    model = models.Pensieve
    form_class = forms.PensieveForm
    template_name = 'pensieve/update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in', None):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)

    def get_initial(self):
        initial = super(PensieveUpdate, self).get_initial()
        initial['up'] = self.request.session.get('up', None)
        return initial



class PensieveDelete(generic.DeleteView):
    model = models.Pensieve
    template_name = 'pensieve/delete.html'
    success_url = reverse_lazy('pensieve:list')

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('checked_in', None):
            return redirect('/gate/')

        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)
