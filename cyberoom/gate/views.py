# coding = utf8

from django.shortcuts import render, redirect
from . import models, forms
import hashlib
import base64
import requests
import json


# 生成密钥
def get_password(id, paswd):
    idBase = base64.b64encode(id.encode()).decode()
    paswdBase = base64.b64encode(paswd.encode()).decode()
    mixBase = base64.b85encode((paswdBase + idBase).encode()).decode()
    theKey = hashlib.sha3_256(mixBase.encode()).hexdigest()[24:60]
    return theKey


# 获取bing每日壁纸
def get_the_wallpaper():
    bingURL = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/52.0.2743.116 Edge/15.15063'
    }
    wallJson = requests.get(bingURL, headers).text
    wallURL = json.loads(wallJson)['images'][0]['url']
    wallFullURL = 'http://cn.bing.com' + wallURL
    return wallFullURL


# 登录
def step_in(request):
    # 检查登陆状态
    if request.session.get('checked_in', None):
        return redirect('/path/')

    theWall = get_the_wallpaper()

    if request.method == 'POST':
        tempGateForm = forms.GateForm(request.POST)
        message = 'check what u input'
        if tempGateForm.is_valid():
            nameGText = tempGateForm.cleaned_data.get('nameGForm')
            passGText = tempGateForm.cleaned_data.get('passGForm')
            genKey = get_password(nameGText, passGText)
            unlock = models.TheKey.objects.filter(shape=genKey)
            if unlock:
                request.session['checked_in'] = True
                return redirect('/path/')
            else:
                message = 'stay away from here'
                return render(request, 'gate.html', locals())
        else:
            return render(request, 'gate.html', locals())

    tempGateForm = forms.GateForm()
    return render(request, 'gate.html', locals())


# 注册
def check_in(request):
    if request.session.get('checked_in', None):
        return redirect('/path/')

    theWall = get_the_wallpaper()

    if request.method == 'POST':
        tempSecureForm = forms.SecureForm(request.POST)
        message = 'check what u input'
        if tempSecureForm.is_valid():
            nameSText = tempSecureForm.cleaned_data.get('nameSForm')
            passSText = tempSecureForm.cleaned_data.get('passSForm')
            checkSText = tempSecureForm.cleaned_data.get('checkSForm')
            room = models.TheKey.objects.filter(owner=nameSText)
            harmlessnessDeclaration = ['黑域', '光墓', '慢雾', '无故事王国', '低光速黑洞']
            if room:
                message = 'gone boy'
                return render(request, 'secure.html', locals())
            elif checkSText not in harmlessnessDeclaration:
                message = 'The Three-Body Problem'
                return render(request, 'secure.html', locals())
            else:
                newGuest = models.TheKey()
                theKey = get_password(nameSText, passSText)
                newGuest.owner = nameSText
                newGuest.shape = theKey
                newGuest.save()
                return redirect('/')
        else:
            return render(request, 'secure.html', locals())

    tempSecureForm = forms.SecureForm()
    return render(request, 'secure.html', locals())


# 索引界面
def the_path(request):
    if not request.session.get('checked_in', None):
        return redirect('/')

    return render(request, 'path.html')


# 登出
def see_you(request):
    if not request.session.get('checked_in', None):
        return redirect('/')

    request.session.flush()
    return redirect('/')
