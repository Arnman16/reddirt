from rest_framework import serializers
from ..models import Subreddit, Post, PostVotes


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
