from rest_framework import serializers
<<<<<<< HEAD
from .models import Article

=======
from .models import Article, Comment
>>>>>>> article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
<<<<<<< HEAD
        field = "__all__"
=======
        fields = ['id', 'title', 'content', 'author', 'create_at', 'update_at', 'like_users', 'favorites']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'content']
>>>>>>> article
