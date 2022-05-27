from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.db import models

from .permissions import PotomPridumayuNazvanie
from .models import Post, Comment, Category, Rating
from .serializers import (
    PostSerializers,
    PostDetailSerializers,
    CommentCreateSerializers,
    CategoriesSerializers,
    RatingSerializers,
)
from .service import PaginationPosts


# def auth(request):
#     return render(request, 'prod/github.html')


class PostListView(generics.ListCreateAPIView):
    """Вывод всех новостей"""

    serializer_class = PostSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ['author', 'category']
    search_fields = ['title']
    lookup_field = 'slug'
    # pagination_class = PaginationPosts

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        posts = Post.objects.filter(is_published=True
        ).annotate(
            user_rating=models.Count('post_id', filter=models.Q(post_id__user=self.request.user))
        ).annotate(
            middle_rating=(models.Avg('post_id__rating'))
        )
        return posts


class PostDetailView(generics.RetrieveAPIView, 
                     generics.DestroyAPIView, 
                     generics.UpdateAPIView):
    """Вывод конкретного поста"""

    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostDetailSerializers
    lookup_field = 'slug' 
    permission_classes = [PotomPridumayuNazvanie]


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


class RatingView(generics.ListCreateAPIView):
    """Вывод рейтинга"""
    
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        serializers = RatingSerializers(data=request.data)
        if serializers.is_valid():
            self.perform_create(serializers)
            return Response(status=201)
        else:
            return Response(status=400)