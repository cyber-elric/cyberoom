# coding=utf-8

from django.shortcuts import redirect
from django.views import generic
from . import forms, models
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
import hashlib
import os
import time


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

    # 自动为用户处理pensieve的作者
    def get_initial(self):
        initial = super(PensieveCreate, self).get_initial()
        initial['up'] = self.request.session.get('up', None)
        return initial

    # def get_context_data(self, **kwargs):
    #     context = super(PensieveCreate, self).get_context_data(**kwargs)
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

    # def get_context_data(self, **kwargs):
    #     context = super(PensieveUpdate, self).get_context_data(**kwargs)
    #     context['uper'] = forms.PensieveForm(initial={
    #         'up': self.request.session.get('up', None),
    #     })
    #     return context


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


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        fileObject = request.FILES['file']
        fileNameSuffix = fileObject.name.split(".")[-1]
        if fileNameSuffix not in ["jpg", "png", "gif", "jpeg", "mp4",]:
            return JsonResponse({"message": "错误的文件格式"})
 
        path = os.path.join(settings.MEDIA_ROOT, 'tinymce')
        # 如果没有这个路径则创建
        if not os.path.exists(path):
            os.makedirs(path)

        m = hashlib.sha3_256()
        m.update(str(time.time()).encode())
        fileName = m.hexdigest() + '.' + fileObject.name.split('.')[-1]

        filePath = os.path.join(path, fileName)
        fileURL = f'{settings.MEDIA_URL}tinymce/{fileName}'
 
        if os.path.exists(filePath):
            return JsonResponse({
                "message": "文件已存在",
                'location': fileURL
            })
 
        with open(filePath, 'wb+') as f:
            for chunk in fileObject.chunks():
                f.write(chunk)
 
        return JsonResponse({
            'message': '上传图片成功',
            'location': fileURL
        })
    return JsonResponse({'detail': "错误的请求"})
