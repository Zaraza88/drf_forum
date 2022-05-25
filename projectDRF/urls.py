from django.contrib import admin
from django.urls import path, include

# from prod.views import auth


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('prod.urls')),
    # path('', include('social_django.urls', namespace='social')),
    # path('auth/', auth, name='auth'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
]
