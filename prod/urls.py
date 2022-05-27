from django.urls import path

from . import views


urlpatterns = [
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    path('comment/', views.CreateComment.as_view(), name='comment'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    path('rating/', views.RatingView.as_view())
]
