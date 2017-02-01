from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from comments.api.serializers import CommentCreateSerializer, DetailCommentSerializer, CommentSerializer
from comments.models import Comment
from posts.api.permissions import IsOwnerOrReadOnly


class CommentCreate(CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('parent_comment')
        if comment:
            parent_comment = Comment.objects.get(id=comment)
            if int(request.POST.get('parent')) != parent_comment.parent.id:
                return Response('Post id of comment and reply comment must match!')
        return super(CommentCreate, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentRUD(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['content']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DetailCommentSerializer(instance, context={'request': self.request})
        return Response(serializer.data)


