from rest_framework import serializers
from .models import Article, Comment, ArticleView


class ArticleSerializer(serializers.ModelSerializer):
    like_users_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'url', "author_username",
                  'like_users_count', 'favorites_count']

    def get_like_users_count(self, instance):
        return instance.like_users.count()

    def get_favorites_count(self, instance):
        return instance.favorites.count()

    def get_author_username(self, obj):
        return obj.author.username

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        article_views_count = ArticleView.objects.filter(
            article=instance).count()  # ArticleView의 개수를 세기
        ret['article_views'] = article_views_count  # 결과에 article_views 필드 추가
        return ret


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'article', 'content', "author_username", "comments"]

    def get_author_username(self, obj):
        return obj.author.username
    
    def get_comments(self, obj):
        sub_comments = Comment.objects.filter(parent_comment=obj)
        serializer = CommentSerializer(sub_comments, many=True)
        return serializer.data


class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'url', "author_username",
                  'like_users_count', 'favorites_count', 'comments', 'comments_count']
