from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from articles.models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",

            "password",
            "password_question",
            "password_answer",
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
        

    def create(self, validated_data):
        # 받아온 비밀번호를 해시로 변환
        hashed_password = make_password(validated_data['password'])
        # 변환된 해시를 validated_data에 업데이트
        validated_data['password'] = hashed_password
        return super().create(validated_data)

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if "username" in attrs:
            if get_user_model().objects.filter(username=attrs["username"]).exists():
                raise serializers.ValidationError("username exists")
        if "email" in attrs:
            if get_user_model().objects.filter(email=attrs["email"]).exists():
                raise serializers.ValidationError("email exists")
        if not "password_question" in attrs:
            raise serializers.ValidationError("password_question is required ")
        if not "password_answer" in attrs:
            raise serializers.ValidationError("password_answer is required")

        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    like_articles = serializers.SerializerMethodField()
    favorite_articles = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "like_articles",
            "favorite_articles",
        ]

    def get_like_articles(self, user):
        # 사용자가 좋아요한 글을 가져오는 로직
        return [article.title for article in Article.objects.filter(like_users=user)]

    def get_favorite_articles(self, user):
        # 사용자가 즐겨찾기한 글을 가져오는 로직
        return [article.title for article in Article.objects.filter(favorites=user)]

