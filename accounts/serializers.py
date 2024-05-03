from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'name', 'nickname', 'birthday', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user