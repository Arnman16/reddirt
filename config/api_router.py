from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reddit.users.api.views import UserViewSet
from reddit.posts.api.views import PostViewSet, AllPostsViewSet, PostVotesViewSet, CommentViewSet, CommentViewSetReadOnly

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("allposts", AllPostsViewSet, basename='allposts')
router.register("posts", PostViewSet)
router.register("post_votes", PostVotesViewSet)
router.register("comments", CommentViewSet)
router.register("comments_read_only", CommentViewSetReadOnly, basename="comments_read_only")



app_name = "api"
urlpatterns = router.urls
