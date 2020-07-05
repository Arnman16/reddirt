from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Subreddit, Post, PostVotes, PostComment

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    subreddit = serializers.PrimaryKeyRelatedField(
        queryset=Subreddit.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "created",
            "modified",
            'time_since_post',
            "title",
            "link",
            "description",
            "description_br",
            "owner",
            'score',
            "username",
            "owner_url",
            "subreddit",
            "subreddit_name",
            'slug',
            'subreddit_slug',
            'full_url',
            'user_vote',
        ]
        extra_kwargs = {
            "url": {"view_name": "api:posts", "lookup_field": "title"}
        }
        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }


class PostVotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVotes
        fields = ['post_id', 'user_id', 'vote', 'up_color', 'down_color', 'id',
                  ]


class AllPostsSerializer(serializers.ModelSerializer):
    subreddit = serializers.PrimaryKeyRelatedField(
        queryset=Subreddit.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "created",
            "modified",
            'time_since_post',
            "title",
            "link",
            "description",
            "description_br",
            "owner",
            "username",
            "owner_url",
            "subreddit",
            "subreddit_name",
            'slug',
            'subreddit_slug',
            'score',
            'full_url',
            'user_vote',
            'user_up_style',
            'user_down_style',
        ]
        extra_kwargs = {
            "url": {"view_name": "api:allposts", "lookup_field": "title"}
        }
        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_children")

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    parent = serializers.PrimaryKeyRelatedField(
        queryset=PostComment.objects.all())

    class Meta:
        model = PostComment
        fields = [
            "id",
            "post_id",
            "created",
            "modified",
            'time_since_comment',
            "comment",
            "comment_br",
            "user_id",
            "username",
            "owner_url",
            'score',
            'user_vote',
            'user_up_style',
            'user_down_style',
            'level',
            'parent',
            'children',
        ]

        extra_kwargs = {
            "url": {"view_name": "api:allposts", "lookup_field": "title"}
        }

    def get_children(self, obj):
        """ self referral field """
        serializer = CommentSerializer(
            instance=obj.comment_reply.all(),
            many=True
        )
        return serializer.data
