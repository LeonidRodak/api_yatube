from rest_framework import viewsets
# Пользователь должен быть авторизован
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

# Импортирует наши классы
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    # ModelViewSet автоматически предоставляет все методы
    """Работа с постами (обязательно ModelViewSet, как требует задание)"""

    # Запрос к базе для ViewSet
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

    # self - это сам объект CommentViewSet
    def get_queryset(self):
        """Переопределяем, чтобы показывать комментарии только к конкретному посту"""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        """При создании комментария подставляем автора и пост"""
        post = self.get_post()
        # Явно передаём post, потому что поле read_only в сериализаторе
        serializer.save(author=self.request.user, post=post)

    def get_post(self):
        """Выносим получение поста в отдельный метод (по чек-листу)"""
        # self.kwargs - это параметры из URL (например, post_id=15)
        post_id = self.kwargs.get("post_id")
        return get_object_or_404(Post, id=post_id)
