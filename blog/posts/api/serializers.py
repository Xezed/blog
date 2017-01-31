from rest_framework import serializers, pagination

from comments.models import Comment
from posts.models import Post


class ChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name='comments-api:comment-api')

    class Meta:
        model = Comment
        fields = ('user', 'url', 'content', 'pub_date',)


class DetailCommentSerializer(ChildCommentSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(ChildCommentSerializer.Meta):
        fields = ('user', 'content', 'pub_date', 'replies')

    def get_replies(self, obj):
        if obj.has_children:
            return ChildCommentSerializer(obj.children(), many=True, context={'request': self.context['request']}).data
        return None


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    replies = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'url', 'content', 'pub_date', 'replies')
        extra_kwargs = {
            'url': {'view_name': 'comments-api:comment-api'}
        }

    def get_replies(self, obj):
        return Comment.children(obj).count()


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
