from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnloR
from .models import Post, Comment, Category
from .serializers import (
    PostSerializers,
    PostDetailSerializers,
    CommentCreateSerializers,
    CategoriesSerializers,
)


def auth(request):
    return render(request, 'prod/github.html')


class PostListView(generics.ListCreateAPIView):
    """Вывод всех новостей"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializers

    permission_classes = [IsAuthorOrReadOnloR]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['author', 'category']
    search_fields = ['title']
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveAPIView, 
                     generics.DestroyAPIView, 
                     generics.UpdateAPIView):
    """Вывод конкретной новости"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostDetailSerializers
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
    
