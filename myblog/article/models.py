from django.db import models
# Django本身內建的User模型。
from django.contrib.auth.models import User
# timezone處理時間相關
from django.utils import timezone
# class Article處理所有文章相關的數據
class ArticlePost(models.Model):
    # 文章作者author透過外鍵models.ForeignKey與內建User模型連結到一起，on_delete指定資料同步刪除
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章標題
    title = models.CharField(max_length=100)

    # 文章內文
    body = models.TextField()

    # 創建文章的時間
    created = models.DateTimeField(default=timezone.now)

    # 定義model的metadata
    class Meta:
    	# 數據以倒序排列
        ordering = ('-created',)

    # 返回文章標題
    def __str__(self):
        return self.title