from django.urls import path, include
from rest_framework import routers

from . import views


# router = routers.SimpleRouter()
# router.register(r'post', views.PostViewSet)

urlpatterns = [
    # path('', include(router.urls)),

    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    path('comment/', views.CreateComment.as_view(), name='comment'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),

    path('rating/', views.RatingView.as_view())
    # path('categories/<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail')
]

# {
#     "email": "test@gmai.com",
#     "text": "texttext",
#     "post": 3
# }