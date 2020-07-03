from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import Subreddit, Post

class PostView(DetailView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'posts/post_view.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the data
        context['subreddits'] = Subreddit.objects.all()
        return context

class SubredditView(DetailView):
    model = Subreddit
    template_name = 'posts/subreddit_view.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the data
        obj = self.get_object().id
        context['posts'] = Post.objects.filter(subreddit=obj)
        context['subreddits'] = Subreddit.objects.all()
        return context

class AllSubredditsView(TemplateView):
    model = Subreddit
    template_name = 'posts/subreddit_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['subreddits'] = Subreddit.objects.all()
        context['page'] = "all"
        return context

class FrontPageView(TemplateView):
    model = Subreddit
    template_name = 'posts/subreddit_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['subreddits'] = Subreddit.objects.all()
        context['page'] = "frontpage"
        return context