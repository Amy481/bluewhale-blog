from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 登入
    path('login/', views.user_login, name='login'),
    # 登出
    path('logout/', views.user_logout, name='logout'),
    # 用戶註冊
    path('register/', views.user_register, name='register'),
    # 用户删除
    path('delete/', views.user_delete, name='delete'),
]