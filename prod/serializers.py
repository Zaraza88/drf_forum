from unicodedata import category
from rest_framework import serializers

from .models import Post, Category, Comment, User, Rating
from .mixins import MixinCommentSerealizers


class RatingSerializers(serializers.ModelSerializer):
    """Добавление рейтинга"""

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['rating', 'user', 'post_id']

    def create(self, validated_data):
        rating_post = Rating.objects.update_or_create(
            user=validated_data.get('user'),
            post_id=validated_data.get('post_id'),
            defaults={'rating': validated_data.get('rating')}
        )
        return rating_post


class FilterRewiewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializar(serializers.Serializer):
    """Рекурсивный вывод дочерник отзывов"""

    def to_representation(self, instance):
        serializers = CommentViewSerealizers(instance, context=self.context)
        return serializers.data


class CommentCreateSerializers(MixinCommentSerealizers, serializers.ModelSerializer):
    """Добавляем комментарии к посту"""

    class Meta:
        model = Comment
        exclude = ['date', 'parent']


class CommentViewSerealizers(MixinCommentSerealizers, serializers.ModelSerializer):
    """Вывод комментариев"""

    children = RecursiveSerializar(many=True)

    class Meta:
        list_serializer_class = FilterRewiewListSerializer
        model = Comment
        fields = ['name', 'text', 'children']


class PostSerializers(serializers.ModelSerializer):
    """Вывод всех постов"""

    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    user_rating = serializers.BooleanField()
    middle_rating = serializers.IntegerField()

    class Meta:
        model = Post
        exclude = ['slug', 'date_of_creation',
                   'is_published', 'publication_date']


class PostDetailSerializers(serializers.ModelSerializer):
    """Вывод конкретной поста"""

    post_review = CommentViewSerealizers(many=True)
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    post_id = RatingSerializers(many=True)

    class Meta:
        model = Post
        fields = ['title', 'category', 'author',
                  'content', 'post_review', 'post_id']
        lookup_field = 'slug'


class CategoriesSerializers(serializers.ModelSerializer):
    """Вывод всех категорий"""

    class Meta:
        model = Category
        fields = ['title']
