from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm

# 登入
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            # 檢查帳號密碼是否在數據庫中有符合項目
            if user:
                # 有對應資料則登入
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("帳號或密碼有錯，請重新輸入")
        else:
            return HttpResponse("帳號或密碼不合規")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse("請使用GET或POST")

# 登出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")