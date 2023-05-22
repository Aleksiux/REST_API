from django.contrib import admin
from .models import Comment, CommentLike, Post, PostLike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
