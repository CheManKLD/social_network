from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import PostSerializer


class PostAPIPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostAPIViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('likes')
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly, )
    pagination_class = PostAPIPagination

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated], name='{basename}-like')
    def like(self, request, pk=None):
        try:
            post = self.get_object()
        except:
            return Response(data={'error': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND)

        post_likes = post.likes.all()

        if post_likes and self.request.user in post_likes:
            return Response(data={'error': 'The post already liked'}, status=status.HTTP_409_CONFLICT)

        post.likes.add(self.request.user)
        return Response({'likes': len(post_likes) + 1})

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated], name='{basename}-unlike')
    def unlike(self, request, pk=None):
        try:
            post = self.get_object()
        except:
            return Response(data={'error': 'The post does not exist'}, status=status.HTTP_404_NOT_FOUND)

        post_likes = post.likes.all()

        if post_likes and self.request.user in post_likes:
            post.likes.remove(self.request.user)
            return Response({'likes': len(post_likes) - 1})

        return Response(data={'error': 'The post already unliked'}, status=status.HTTP_409_CONFLICT)
