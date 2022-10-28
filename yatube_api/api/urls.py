from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'posts', PostViewSet)
v1_router.register(r'groups', GroupViewSet)
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)
v1_router.register(r'follow', FollowViewSet, basename='following')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
