from django.db import models
from django.conf import settings

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    url = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_articles")
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="favorite_articles")

    def __str__(self) -> str:
        return self.title


class ArticleView(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_views')

    class Meta:
        unique_together = ('article', 'user')


class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name="comments", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, related_name='replies')
