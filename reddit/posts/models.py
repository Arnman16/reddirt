from django.db.models import CharField, TextField, Model, ForeignKey, URLField, IntegerField, ManyToManyField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta


class Subreddit(TimeStampedModel):
    name = CharField(max_length=56, help_text='Enter subreddit name')
    path = CharField(max_length=20, help_text='Enter subreddit url path')
    slug = AutoSlugField(
        "subreddit url slug",
        unique=True,
        always_update=False,
        populate_from="path")
    description = TextField("Subreddit Description", blank=True)
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True)

    # Metadata
    class Meta:
        ordering = ['-slug']

    # Methods
    def get_absolute_url(self):
        return reverse('reddit:subreddit', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.slug)

class Post(TimeStampedModel):
    title = CharField(max_length=32, help_text='Enter Post Title')
    link = URLField("Submit link to content", blank=True)
    description = TextField("Post Description", blank=True)
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False)
    subreddit = ForeignKey(Subreddit,
                        on_delete=models.CASCADE,
                        null=False)

    slug = AutoSlugField(
        "Post url slug",
        unique=True,
        always_update=False,
        populate_from="title")
    user_vote = 0
    user_up_style = ''
    user_down_style = ''
    # Metadata
    class Meta:
        ordering = ['-modified']

    # Methods
    def get_absolute_url(self):
        return reverse('reddit:post', kwargs={'slug': self.slug, 'subreddit_slug': self.subreddit_slug})

    def __str__(self):
        return self.title

    def get_subreddit(self):
        return self.subreddit.slug

    def get_full_url(self):
        return '/r/' + self.subreddit.slug + '/' + self.slug

    def username(self):
        return self.owner.username

    def subreddit_name(self):

        return self.subreddit.name

    def time_since_post(self):
        e = ''
        if self.modified != self.created:
            e = '*'
        time_now = datetime.now(timezone.utc)
        diff_time = time_now - self.modified
        diff_days, diff_hours, diff_mins = str(diff_time.days), str(int(diff_time.seconds / 3600)), str(int(diff_time.seconds / 60))
        if diff_days == '0':
            if int(diff_mins) < 60:
                if diff_mins == '1':
                    return e+'1 minute ago.'
                return e+diff_mins + ' minutes ago.'
            if diff_hours == '1':
                return e+'1 hour ago'
            return e+diff_hours + ' hours ago.'
        if diff_days == '1':
            return e+'1 day ago.'
        return e+diff_days + ' days ago.'

    def owner_url(self):
        return '/users/' + self.owner.username

    def description_br(self):
        safe_text = self.description.replace('<', '').replace('>', '').replace(
            '{{', '').replace('{%', '').replace('}}', '').replace('%}', '')
        safe_text = safe_text.replace('((b))', '<strong>').replace(
            '((/b))', '</strong>').replace('((i))', '<i>').replace('((/i))', '</i')
        return "<br>".join(safe_text.splitlines())

    def score(self):
        votes = PostVotes.objects.filter(post_id=self.id)
        score = 0
        for vote in votes:
            score = score + vote.vote
        return score
    score = score


    def age_in_days(self):
        time_now = datetime.now(timezone.utc)
        diff_time = time_now - self.created
        days_since_post, secs_since_post = diff_time.days, diff_time.seconds
        days_since_post_float = secs_since_post / 86400 + days_since_post
        return days_since_post_float

    def weighted_score(self):
        if self.score() == 0:
            return 0
        time_now = datetime.now(timezone.utc)
        diff_time = time_now - self.created
        days_since_post, secs_since_post = diff_time.days, diff_time.seconds
        days_since_post_float = secs_since_post / 86400 + days_since_post
        return self.score() / days_since_post_float

    subreddit_slug = get_subreddit
    full_url = get_full_url


class PostVotes(Model):
    class Meta:
        unique_together = (('post_id', 'user_id'),)
    post_id = ForeignKey('Post', related_name='post', on_delete=models.CASCADE)
    user_id = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False)
    VOTE_CHOICES = [(-1, 'downvote'), (0, 'no vote'), (1, 'upvote')]
    vote = IntegerField(choices=VOTE_CHOICES, default=None)

    def up_color(self):
        if self.vote == 1:
            return 'orange'
        return 'grey'

    def down_color(self):
        if self.vote == -1:
            return 'blue'
        return 'grey'


class PostComment(TimeStampedModel):
    class Meta:
        ordering = ['-modified']
    post_id = ForeignKey('Post', related_name='comment_post', on_delete=models.CASCADE, null=False)
    user_id = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False)
    comment = TextField("Post Comment", blank=True)
    user_vote = 0
    user_up_style = ''
    user_down_style = ''
    tldr = CharField(max_length=56, help_text="Too Long; Didn't Read. Your responce in a nutshell")
    parent = ForeignKey('PostComment', related_name='comment_reply', on_delete=models.CASCADE, null=True, blank=True)
    def children(self):
        return self.comment_reply.all()

    def level(self):
        if self.parent:
            return self.parent.level() + 1
        return 0

    def username(self):
        return self.user_id.username

    def time_since_comment(self):
        time_now = datetime.now(timezone.utc)
        diff_time = time_now - self.modified
        diff_days, diff_hours = str(diff_time.days), str(int(diff_time.seconds / 3600))
        if diff_days == '0':
            if diff_hours == '1':
                return '1 hour ago'
            return diff_hours + ' hours ago.'
        else:
            if diff_days == '1':
                return '1 day ago.'
            return diff_days + ' days ago.'

    def owner_url(self):
        return '/users/' + self.user_id.username

    def comment_br(self):
        safe_text = self.comment.replace('<', '').replace('>', '').replace(
            '{{', '').replace('{%', '').replace('}}', '').replace('%}', '')
        safe_text = safe_text.replace('((b))', '<strong>').replace(
            '((/b))', '</strong>').replace('((i))', '<i>').replace('((/i))', '</i')
        return "<br>".join(safe_text.splitlines())

    def score(self):
        votes = PostVotes.objects.filter(post_id=self.id)
        score = 0
        for vote in votes:
            score = score + vote.vote
        return score
    def __str__(self):
        if len(self.comment) > 20:
            return self.comment[:20] + '...'
        return self.comment
    
    score = score
