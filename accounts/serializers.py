from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

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
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
        ]
