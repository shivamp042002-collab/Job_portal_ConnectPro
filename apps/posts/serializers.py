from rest_framework import serializers
from .models import Post, Like, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model  = Comment
        fields = [
            'id', 'author_username', 'content',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author_username', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count     = serializers.SerializerMethodField()
    comments_count  = serializers.SerializerMethodField()
    is_liked        = serializers.SerializerMethodField()
    comments        = CommentSerializer(many=True, read_only=True)

    class Meta:
        model  = Post
        fields = [
            'id', 'author_username', 'content', 'image',
            'likes_count', 'comments_count', 'is_liked',
            'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author_username', 'likes_count',
            'comments_count', 'is_liked', 'created_at', 'updated_at'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = ['id', 'content', 'image']
        read_only_fields = ['id']