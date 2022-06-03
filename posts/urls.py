from django.urls import path, include
from rest_framework import routers

from posts.routers import PostCustomRouter
from posts.views import PostAPIViewSet

router = PostCustomRouter()
router.register(r'post', PostAPIViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
