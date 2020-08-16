# coding = utf8

from django.shortcuts import render, redirect
from . import models, forms
import hashlib
import base64
import requests
import json
from os.path import exists
from os import stat
from time import strftime, localtime


# 生成密钥
def get_password(id, paswd):
    idBase = base64.b64encode(id.encode()).decode()
    paswdBase = base64.b64encode(paswd.encode()).decode()
    mixBase = base64.b85encode((paswdBase + idBase).encode()).decode()
    theKey = hashlib.sha3_256(mixBase.encode()).hexdigest()[24:60]
    return theKey


# 登录
def step_in(request):
    # 检查登陆状态，下同
    if request.session.get('checked_in', None):
        return redirect('/')

    theWall = get_the_wallpaper()  # 壁纸地址

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
                request.session['up'] = nameGText
                return redirect('/')
            else:
                message = 'stay away from here'
                return render(request, 'gate/gate.html', locals())
        else:
            return render(request, 'gate/gate.html', locals())

    tempGateForm = forms.GateForm()
    return render(request, 'gate/gate.html', locals())


# 注册
def check_in(request):
    if request.session.get('checked_in', None):
        return redirect('/')

    theWall = get_the_wallpaper()

    if request.method == 'POST':
        tempSecureForm = forms.SecureForm(request.POST)
        message = 'check what u input'
        if tempSecureForm.is_valid():
            nameSText = tempSecureForm.cleaned_data.get('nameSForm')
            passSText = tempSecureForm.cleaned_data.get('passSForm')
            checkSText = tempSecureForm.cleaned_data.get('checkSForm')
            safeSText = tempSecureForm.cleaned_data.get('safeSForm')
            harmlessnessDeclaration = ['黑域', '光墓', '慢雾', '无故事王国', '低光速黑洞']
            room = models.TheKey.objects.filter(owner=nameSText)  # 检查用户名是否已被注册
            if room:
                message = 'you are late'
                return render(request, 'gate/secure.html', locals())
            elif passSText != checkSText:
                message = '2 passwords not match'
            elif safeSText not in harmlessnessDeclaration:
                message = 'The Three-Body Problem'
                return render(request, 'gate/secure.html', locals())
            else:
                newGuest = models.TheKey()
                theKey = get_password(nameSText, passSText)
                newGuest.owner = nameSText
                newGuest.shape = theKey
                newGuest.save()
                return redirect('/gate/')
        else:
            return render(request, 'gate/secure.html', locals())

    tempSecureForm = forms.SecureForm()
    return render(request, 'gate/secure.html', locals())


# 索引界面
def the_path(request):
    if not request.session.get('checked_in', None):
        return redirect('/gate/')

    return render(request, 'gate/path.html')


# 登出
def see_you(request):
    if not request.session.get('checked_in', None):
        return redirect('/gate/')

    request.session.flush()
    return redirect('/gate/')


def page_not_found(request, exception):
    return render(request, '404.html')


def page_error(request):
    return render(request, '404.html')


# 获取bing每日壁纸
def get_the_wallpaper():
    bingURL = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/52.0.2743.116 Edge/15.15063'
    }
    try:
        wallJson = requests.get(bingURL, headers).text
        wallURL = json.loads(wallJson)['images'][0]['url']
        wallFullURL = 'http://cn.bing.com' + wallURL
        return wallFullURL
    except:
        pass


# 获取bing每日壁纸,下载图片模式
# def get_the_wallpaper():
#     fileName = '/home/cybura/cyberoom/cyberoom/avalon/bing.jpg'
#     if not exists(fileName) or strftime("%Y%m%d", localtime(stat(fileName).st_mtime)) != strftime("%Y%m%d", localtime()):
#         bingURL = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/52.0.2743.116 Edge/15.15063'
#         }
#         try:
#             wallJson = requests.get(bingURL, headers).text
#             wallURL = json.loads(wallJson)['images'][0]['url']
#             wallFullURL = 'http://cn.bing.com' + wallURL
#             response = requests.get(wallFullURL)
#             with open(fileName, 'wb') as f:
#                 f.write(response.content)
#         except:
#             pass

#     return "/avalon/bing.jpg"
