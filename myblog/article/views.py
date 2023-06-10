from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
import markdown
from django.contrib.auth.decorators import login_required

# 文章主頁
def article_main(request):
    articles = ArticlePost.objects.all().order_by('author__username')
    context = {'articles': articles}
    return render(request, 'article/main.html', context)

# 文章詳細內容
def article_detail(request, id):
    # 如果用戶已登入
    article = ArticlePost.objects.get(id=id)
    # 讓html可適應markdown語法
    article.body = markdown.markdown(article.body, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
    context = {'article': article}
    return render(request, 'article/detail.html', context)

#文章列表
@login_required(login_url='userprofile:login')
def article_list(request):
    user = request.user
    articles = ArticlePost.objects.filter(author=user)
    context = {'articles': articles}
    return render(request, 'article/list.html', context)




# 創建文章
@login_required(login_url='userprofile:login')
def article_create(request):
    # 用戶提交數據(POST)
    if request.method == "POST":
        # 將用戶提交的數據給article_post_form
        article_post_form = ArticlePostForm(data=request.POST)
        # 判斷article_post_form內容是否有標題和內文且符合限制
        if article_post_form.is_valid():
            # 將數據內容保存
            new_article = article_post_form.save(commit=False)
            # 將提交數據的用戶定義為作者
            new_article.author = request.user
            # 將數據內容保存到資料庫
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("內容有誤，請重新填寫。")
    # 用戶請求數據(GET)
    else:
        # 創建表單
        article_post_form = ArticlePostForm()
        # 給予數據內容
        context = { 'article_post_form': article_post_form }
        return render(request, 'article/create.html', context)


# 刪除文章
@login_required(login_url='userprofile:login')
def article_delete(request, id):
    # 根據id刪除對應文章
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")


# 更新文章
@login_required(login_url='userprofile:login')
def article_update(request, id):
    # 獲取文章id
    article = ArticlePost.objects.get(id=id)
    # 用戶提交數據(POST)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            # 儲存新的title和body
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("內容有誤，請重新填寫。")
    # 用戶請求數據(GET)
    else:
        article_post_form = ArticlePostForm()
        # 將原文章內容傳回去
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)