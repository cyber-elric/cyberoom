"""cyberoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('css/', include('css.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import url
# from django.views import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gate.urls')),
    path('captcha/', include('captcha.urls')),
    path('pensieve/', include('pensieve.urls')),
    path('passwords/', include('passwords.urls')),
    path('tinymce/', include('tinymce.urls')),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'gate.views.page_not_found'
handler500 = 'gate.views.page_error'

