from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Comment, PostLike, CommentLike
from rest_framework.exceptions import ValidationError
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response


# class PostList(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('You can\'t edit another user post!')

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You can\'t delete another user post!')


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('You can\'t edit another user comments!')

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You can\'t delete another user comments!')


class PostLikeCreate(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    Method to return specific PostLike objects.
    These are base on the logged in user and specific post in question
    """

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post, user=user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You already likes this comment!')
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You did not left any like in this post!')
