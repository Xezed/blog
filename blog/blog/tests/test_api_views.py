from datetime import timedelta

import pytest
from django.utils import timezone
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from comments.models import Comment
from posts.api.views import PostViewSet
from posts.models import Post

pytestmark = pytest.mark.django_db


@pytest.fixture()
def form_data():
    data = {'title': 'some title', 'content': 'asd7',
            'publish_date_year': 2017, 'publish_date_month': 2, 'publish_date_day': 1}
    return data


@pytest.fixture()
def post_data():
    publisher = mixer.blend('auth.User', username='boss', is_staff=False)
    obj4 = mixer.blend('posts.Post', pk=5, publish_date=timezone.now(), draft=True)
    obj4 = mixer.blend('posts.Post', pk=4, publish_date=timezone.now()+timedelta(days=30))
    obj3 = mixer.blend('posts.Post', pk=1, publish_date=timezone.now(), user=publisher)
    obj2 = mixer.blend('posts.Post', pk=2, publish_date=timezone.now() + timedelta(days=30), user=publisher)
    obj1 = mixer.blend('posts.Post', pk=3, draft=True, user=publisher)
    return obj3, obj2, obj1, publisher


@pytest.fixture()
def comment_data():
    data = {'content': 'Some content', 'parent': 1}
    child_data = {'content': 'cont', 'parent': 1, 'parent_comment': 1}
    child_data2 = {'content': 'conten', 'parent': 2, 'parent_comment': 2}
    return data, child_data, child_data2


class TestPostViewSet:
    def test_get_queryset(self, client, admin_client, post_data):
        req = client.get(reverse('posts:api-list'))
        assert req.status_code == 200
        assert req.data['count'] == 1
        client.force_login(post_data[3])
        req = client.get(reverse('posts:api-list'))
        assert req.data['count'] == 3
        req = admin_client.get(reverse('posts:api-list'))
        assert req.data['count'] == 5

    def test_perform_create(self, data=form_data()):
        factory = APIRequestFactory()
        publisher = mixer.blend('auth.User', username='boss', is_staff=False)
        req = factory.post(reverse('posts:api-list'), data=data)
        req.user = publisher
        resp = PostViewSet.as_view({'post': 'create'})(req)
        assert resp.status_code == 201
        assert Post.objects.count() == 1
        assert Post.objects.first().user == publisher


class TestCommentCreateView:
    def test_post(self, client, post_data, comment_data):
        client.force_login(post_data[3])
        res = client.post(reverse('comments-api:create-api'), data=comment_data[0])
        assert res.status_code == 201
        assert Comment.objects.count() == 1
        assert Comment.objects.first().user == post_data[3]
        res = client.post(reverse('comments-api:create-api'), data=comment_data[1])
        assert Comment.objects.count() == 2
        res = client.post(reverse('comments-api:create-api'), data=comment_data[2])
        assert res.status_code == 400
        assert Comment.objects.count() == 2


class TestCommentRUD:
    def test_retrieve(self, client):
        mixer.blend('comments.Comment', id=1)
        req = client.get(reverse('comments-api:comment-api', kwargs={'pk': 1}))
        assert req.status_code == 200