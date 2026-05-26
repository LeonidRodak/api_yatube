from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Все маршруты, которые мы настроили в api/urls.py (posts, groups, comments, token)
    path("api/v1/", include("api.urls")),
    # В браузере появляется кнопка "Log in" и возможность авторизоваться по токену
    path("api-auth/", include("rest_framework.urls")),
]


if settings.DEBUG:
    # Это позволяет Django отдавать загруженные пользователями файлы в режиме разработки
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # Отдает статические файлы
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
