from django.urls import path, include
# Автоматически создаёт URL-ы для всех ViewSet
from rest_framework.routers import DefaultRouter
# Готовая view от DRF для получения токена
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostViewSet, GroupViewSet, CommentViewSet

# Создаём экземпляр роутера (будет автоматически генерировать URL и маршруты для ViewSet)
router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("groups", GroupViewSet)
# Вложенный роутер для комментариев - именно так требует чек-лист
router.register(
    # r"" чтобы экранировать слеши.
    # (?P<post_id>\d+) - регулярное выражение:
    #     - post_id - имя параметра
    #     - \d+ - одна или больше цифр
    # basename="comment" - обязательно для вложенных ViewSet'ов (нужно для reverse URL)
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)

urlpatterns = [
    # Эндпоинт для получения токена
    path("api-token-auth/", obtain_auth_token),
    # Подключаем все маршруты, которые сгенерировал router
    path("", include(router.urls)),
]
