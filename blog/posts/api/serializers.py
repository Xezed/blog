from rest_framework import serializers, pagination

from comments.models import Comment
from posts.models import Post


class ChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'content', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('user', 'content', 'pub_date', 'replies')

    def get_replies(self, obj):
        return ChildCommentSerializer(obj.children(), many=True).data


class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.SerializerMethodField('paginated_comments')
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
