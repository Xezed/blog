from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from comments.models import Comment
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.serializers import CommentSerializer, DetailCommentSerializer


class CommentRUD(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['content']
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailCommentSerializer(instance, context={'request': self.request})
        return Response(serializer.data)

