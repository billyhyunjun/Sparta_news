from rest_framework import serializers
from .models import Article, Comment, ArticleView


class ArticleSerializer(serializers.ModelSerializer):
    like_users_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'url', "author",
                  'like_users_count', 'favorites_count']

    def get_like_users_count(self, instance):
        return instance.like_users.count()

    def get_favorites_count(self, instance):
        return instance.favorites.count()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        article_views_count = ArticleView.objects.filter(
            article=instance).count()  # ArticleView의 개수를 세기
        ret['article_views'] = article_views_count  # 결과에 article_views 필드 추가
        return ret


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'article', 'content']
        
class ArticleDetailSerializer(ArticleSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source="comments.count", read_only=True)
