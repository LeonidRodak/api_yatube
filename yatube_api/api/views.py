from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Работа с постами (обязательно ModelViewSet, как требует задание)"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """При создании поста автоматически подставляем автора"""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение групп"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()  # через related_name (лучшая практика)

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_post(self):
        """Выносим получение поста в отдельный метод (по чек-листу)"""
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)
