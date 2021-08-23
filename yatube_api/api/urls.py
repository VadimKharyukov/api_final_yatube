from rest_framework import routers
from django.urls import include, path

from .views import GroupViewSet, PostViewSet, CommentViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/jwt/', include('djoser.urls')),
    path('v1/jwt/', include('djoser.urls.jwt')),
]
