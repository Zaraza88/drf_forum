from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment, Category
from .serializers import (
    PostSerializers,
    PostDetailSerializers,
    CommentCreateSerializers,
    CategoriesSerializers,
)


class PostListView(generics.ListCreateAPIView):
    """Вывод всех новостей"""

    # filter_backends = (DjangoFilterBackend,)

    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    # @action(methods=['get'], detail=True)
    # def category(self, request, pk):
    #     category = News.objects.get(pk=pk)
    #     return  Response({'category': category.title})


class PostDetailView(generics.RetrieveAPIView):
    """Вывод конкретной новости"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostDetailSerializers
    lookup_field = 'slug'


class CreateComment(generics.ListCreateAPIView):
    """Добавление комментарий к посту"""

    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(name=self.request.user)


class CategoriesView(generics.ListAPIView):
    """Вывод всех категорий"""

    queryset = Category.objects.all()
    serializer_class = CategoriesSerializers
    permission_classes = [permissions.IsAuthenticated]


# class CategoryDetail(generics.RetrieveAPIView):
#     """Вывод постов конкретной категории"""

#     serializer_class = CetigoryDetailSerializers
#     lookup_field = 'slug'
#     queryset = Category

    # def get_queryset(self):
    #     slug = self.kwargs.get('pk')

    #     return Post.objects.filter(category=slug)
    
