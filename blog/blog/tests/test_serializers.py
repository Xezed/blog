import pytest
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

from comments.api.serializers import CommentSerializer

pytestmark = pytest.mark.django_db


@pytest.fixture()
def comments():
    post = mixer.blend('posts.Post')
    post1 = mixer.blend('posts.Post')
    com1 = mixer.blend('comments.Comment', parent=post)
    com2 = mixer.blend('comments.Comment', parent=post1)
    com3 = mixer.blend('comments.Comment', parent_comment=com1, parent=post)
    com4 = mixer.blend('comments.Comment', parent_comment=com1, parent=post)
    com5 = mixer.blend('comments.Comment', parent_comment=com2, parent=post1)
    com6 = mixer.blend('comments.Comment', parent_comment=com2, parent=post1)
    com7 = mixer.blend('comments.Comment', parent_comment=com1, parent=post)


class TestCommentSerializer:
    def test_get_replies(self, comments, admin_client):
        res = admin_client.get(reverse('posts:api-list'))
        assert res.data['results'][0]['comments'][0]['replies'] == 3
        assert res.data['results'][1]['comments'][0]['replies'] == 2


class TestDetailCommentSerializer:
    def test_get_replies(self, comments, admin_client):
        res = admin_client.get(reverse('comments-api:comment-api', kwargs={'pk': 1}))
        assert len(res.data['replies']) == 3
        res = admin_client.get(reverse('comments-api:comment-api', kwargs={'pk': 2}))
        assert len(res.data['replies']) == 2