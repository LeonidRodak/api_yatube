from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("groups", GroupViewSet)
# Вложенный роутер для комментариев — именно так требует чек-лист
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("api-token-auth/", obtain_auth_token),
    path("", include(router.urls)),
]
