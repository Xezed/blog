from django.db.models.query_utils import Q
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.serializers import PostSerializer
from posts.models import Post


class PostPageNumberPagination(PageNumberPagination):
    page_size = 5


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['title', 'content']
    pagination_class = PostPageNumberPagination
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = None
            return Post.objects.filter(Q(draft=False) |
                                       Q(user=user)
                                       ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
