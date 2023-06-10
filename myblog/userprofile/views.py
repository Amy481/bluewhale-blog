from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm

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

# 用戶註冊
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 設置密碼
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好數據後立即登入並返回博客列表頁面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("註冊表單輸入有誤。請重新輸入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("請使用GET或POST請求數據")