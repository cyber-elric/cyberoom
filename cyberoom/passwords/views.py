# coding = utf8

from django.shortcuts import render, redirect
from . import forms
import hashlib
import base64
import string
import random
# import pyperclip


# 生成密码
def gen_password(request):
    if not request.session.get('checked_in', None):
        return redirect('/')

    if request.method == 'POST':
        tempPasswordForm = forms.PasswordForm(request.POST)
        tempPasswordForm.full_clean()
        idText = tempPasswordForm.cleaned_data.get('protect')
        appText = tempPasswordForm.cleaned_data.get('app')
        lengthText = tempPasswordForm.cleaned_data.get('length')
        check = request.POST.getlist('check')

        # 普通模式
        if idText or appText:
            if lengthText == '':
                length = 12
            elif lengthText.isdigit():
                length = int(lengthText)
                if length > 1000000:
                    length = 1000000
            else:
                message = '长度只认阿拉伯数字'
                return render(request, 'passwd.html', locals())

            idHash = hashlib.sha3_256(idText.encode('utf8')).hexdigest()[:24]
            appHash = hashlib.sha3_256(appText.encode('utf8')).hexdigest()[36:60]
            mixHash = hashlib.sha3_256((appHash + idHash).encode('utf8')).hexdigest()[1:60]
            if check:
                tempString = my_base64_encode(mixHash)
                passwd = base64.b85encode(tempString.encode('utf8')).decode('utf8')[6: length + 6]
            else:
                tempString = base64.b85encode(mixHash.encode('utf8')).decode('utf8')
                passwd = my_base64_encode(tempString)[6: length + 6]
            # pyperclip.copy(passwd)
            return render(request, 'passwd.html', locals())

        else:  # 随机模式
            if lengthText == '':
                length = random.randint(12, 24)
            elif lengthText.isdigit():
                length = int(lengthText)
                if length > 1000000:
                    length = 1000000
            else:
                message = '长度只认阿拉伯数字'
                return render(request, 'passwd.html', locals())
            if check:
                passwdRange = string.punctuation + string.digits + string.ascii_letters
            else:
                passwdRange = string.digits + string.ascii_letters
            passwd = ''
            for i in range(length):
                passwd += random.choice(passwdRange)
            # pyperclip.copy(passwd)
            return render(request, 'passwd.html', locals())

    tempPasswordForm = forms.PasswordForm()
    return render(request, 'passwd.html', locals())


def my_base64_encode(inputs):
    # 自定义base64码表
    myBase64CodeTable = "XC0TBZHSaL3IAFDjRY8J4KPud1tkN2cWVzinrh6vUbOoEQfypsMgweqGmxl957HP"
    translateInputs = str(inputs.encode('utf8'))
    # 将字符串转化为2进制
    binStr = []
    for i in translateInputs:
        x = str(bin(ord(i))).replace('0b', '')
        binStr.append('{:0>8}'.format(x))
    # 输出的字符串
    outputs = ""
    # 不够三倍数，需补齐的次数
    nums = 0
    while binStr:
        # 每次取三个字符的二进制
        tempList = binStr[:3]
        if len(tempList) != 3:
            nums = 3 - len(tempList)
            while len(tempList) < 3:
                tempList += ['0' * 8]
        tempStr = "".join(tempList)
        # 将三个8字节的二进制转换为4个十进制
        tempStrList = []
        for j in range(0, 4):
            tempStrList.append(int(tempStr[j * 6:(j + 1) * 6], 2))
        if nums:
            tempStrList = tempStrList[0:4 - nums]

        for s in tempStrList:
            outputs += myBase64CodeTable[s]
        binStr = binStr[3:]
    outputs += nums * '='
    return outputs
