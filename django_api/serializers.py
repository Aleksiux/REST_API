from rest_framework import serializers
from .models import Post, PostLike, Comment, CommentLike
from django.contrib.auth.admin import User


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    post = serializers.ReadOnlyField(source='post.post_id')

    class Meta:
        model = Comment
        fields = ['comment_id', 'post', 'body', 'created_on', 'user', 'user_id', 'user_email']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'post_id', 'title', 'body', 'user',
            'user_email', 'user_id', 'created_on',
            'comments', 'likes', 'comment_count', 'image']

    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_likes(self, post):
        return PostLike.objects.filter(post=post).count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post_like_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user