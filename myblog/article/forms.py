# 引入表單
from django import forms
# 印入文章模型
from .models import ArticlePost

# 寫文章的表單
class ArticlePostForm(forms.ModelForm):
    class Meta:
        # model數據來自ArticlePost
        model = ArticlePost
        # 表單包含標題和內文兩種內容
        fields = ('title', 'body')