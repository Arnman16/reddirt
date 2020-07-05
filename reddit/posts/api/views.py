from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from .serializers import PostSerializer, AllPostsSerializer, PostVotesSerializer, CommentSerializer
from ..models import Post, Subreddit, PostVotes, PostComment


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class VoteFilter(filters.FilterSet):
    postid_in = NumberInFilter(field_name='post_id', lookup_expr='in')
    queryset = PostVotes.objects.all().order_by('post_id')
    class Meta:
        model = PostVotes
        fields = ['postid_in', ]

class PostViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-id')
    lookup_field = "id"
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'subreddit',
    ]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(owner=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = PostSerializer(request.title, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class AllPostsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = AllPostsSerializer
    queryset = Post.objects.all().order_by('-id')
    lookup_field = "id"
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'subreddit',
    ]

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = PostSerializer(request.title, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class PostVotesViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = PostVotesSerializer
    queryset = PostVotes.objects.all().order_by('post_id')
    lookup_field = "id"
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filter_class = VoteFilter
    filterset_fields = [
        'post_id', 'user_id',
    ]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user_id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = PostVotesSerializer(request.post_id, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class CommentViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet, CreateModelMixin, DestroyModelMixin):
    serializer_class = CommentSerializer
    queryset = PostComment.objects.all()
    lookup_field = "id"
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'post_id',
    ]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user_id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = CommentSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class CommentViewSetReadOnly(ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    queryset = PostComment.objects.filter(parent=None)
    lookup_field = "id"
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'post_id',
    ]

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = CommentSerializer(request.id, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)