from rest_framework import serializers

from comments.models import Comment


class ChildCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    url = serializers.HyperlinkedIdentityField(view_name='comments-api:comment-api')

    class Meta:
        model = Comment
        fields = ('user', 'url', 'content', 'pub_date',)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'parent', 'parent_comment')


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


class DetailCommentSerializer(ChildCommentSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(ChildCommentSerializer.Meta):
        fields = ('user', 'content', 'pub_date', 'replies')

    def get_replies(self, obj):
        if obj.has_children:
            return ChildCommentSerializer(obj.children(), many=True, context={'request': self.context['request']}).data
        return None



