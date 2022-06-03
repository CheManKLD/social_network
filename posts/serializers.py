from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    creation_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    likes = PostLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'creation_date', 'likes')
