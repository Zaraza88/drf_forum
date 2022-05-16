from unicodedata import category
from rest_framework import serializers

from .models import Post, Category, Comment, User
from .mixins import MixinCommentSerealizers


class CommentCreateSerializers(MixinCommentSerealizers, serializers.ModelSerializer):
    """Добавляем комментарии к посту"""

    class Meta:
        model = Comment
        fields = '__all__'


class CommentViewSerealizers(MixinCommentSerealizers, serializers.ModelSerializer):
    """Вывод комментариев"""

    class Meta:
        model = Comment
        fields = ['name', 'email', 'text', 'parent']


class PostSerializers(serializers.ModelSerializer):
    """Вывод всех постов"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        exclude = ['slug', 'date_of_creation', 'is_published']


class PostDetailSerializers(serializers.ModelSerializer):
    """Вывод конкретной поста"""

    post_review = CommentViewSerealizers(many=True)
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ['title', 'category', 'author', 'content', 'post_review']
        lookup_field = 'slug'


class CategoriesSerializers(serializers.ModelSerializer):
    """Вывод всех категорий"""

    class Meta:
        model = Category
        fields = ['title']


# class CetigoryDetailSerializers(serializers.ModelSerializer):
#     """Вывод постов конкретной категории"""

#     category = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Post
#         fields = '__all__'
#         lookup_field = 'slug'
