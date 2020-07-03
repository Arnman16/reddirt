from django.urls import include, path
from .views import PostView, SubredditView, AllSubredditsView, FrontPageView

app_name = 'reddit'

urlpatterns = [
    path("frontpage/", FrontPageView.as_view()),
    path("all/", AllSubredditsView.as_view(), name='all' ),
    path(route='<slug:slug>/', view=SubredditView.as_view(), name='subreddit'),
    path(route='<slug:subreddit_slug>/<slug:slug>', view=PostView.as_view(), name='post'),
]
