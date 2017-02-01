from rest_framework import serializers, pagination

from comments.api.serializers import CommentSerializer
from comments.models import Comment
from posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.SerializerMethodField('paginated_comments',)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ('url', 'id', 'user', 'title', 'content', 'comments', 'publish_date', 'draft', 'image')
        extra_kwargs = {
            'url': {'view_name': 'posts:api-detail'}
        }

    def paginated_comments(self, obj):
        comments = Comment.objects.filter(parent=obj, parent_comment=None)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(comments, self.context['request'])
        serializer = CommentSerializer(page, many=True, context={'request': self.context['request']})
        return serializer.data
