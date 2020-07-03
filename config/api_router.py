from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from reddit.users.api.views import UserViewSet
from reddit.posts.api.views import PostViewSet, AllPostsViewSet, PostVotesViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("allposts", AllPostsViewSet)
router.register("posts", PostViewSet)
router.register("post_votes", PostVotesViewSet)



app_name = "api"
urlpatterns = router.urls
