from rest_framework import serializers
from posts.models import Post, Group, Comment


# ModelSerializer автоматическисоздаёт поля на основе полей модели
class PostSerializer(serializers.ModelSerializer):
    # SlugRelatedField позволяет выводить не id пользователя, а его username
    author = serializers.SlugRelatedField(
        # Для человекочитаемого поля
        slug_field="username", read_only=True
    )
    # Настраиваем поведение класса
    class Meta:
        model = Post
        # Список полей, которые будут присутствовать в JSON
        fields = ["id", "text", "author", "image", "group", "pub_date"]


class GroupSerializer(serializers.ModelSerializer):
    # Нет никаких связей с другими моделями, поэтотму SlugRelatedField не нужен
    class Meta:
        model = Group
        fields = ["id", "title", "slug", "description"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "author", "post", "text", "created"]
        # Для того чтобы комментарий был написан к определенному посту (определается автоматически), а не для любого
        read_only_fields = ["post"]
