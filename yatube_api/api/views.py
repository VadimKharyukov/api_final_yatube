from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS,
    IsAuthenticated
)

from posts.models import Group, Post, Follow

from .serializers import GroupSerializer, PostSerializer, CommentSerializer, \
    FollowSerializer


class IsAuthorOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        post = get_object_or_404(Post,
                                 pk=self.kwargs.get('post_id'))
        serializer.save(post=post,
                        author=self.request.user)

    def get_queryset(self):
        post = get_object_or_404(Post,
                                 pk=self.kwargs.get('post_id'))
        return post.comments


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
