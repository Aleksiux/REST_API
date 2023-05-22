from rest_framework import serializers
from .models import Post, PostLike, Comment, CommentLike


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Post
        fields = ['post_id', 'title', 'body', 'user', 'user_email', 'user_id', 'created_on']

