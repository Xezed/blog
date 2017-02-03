import json
from datetime import timedelta

import pytest
from django.utils import timezone
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture()
def form_data():
    data = {'title': 'some title', 'content': 'asd7',
            "publish_date": "2017-01-24T00:00:00Z"}
    return data


@pytest.fixture()
def post_data():
    publisher = mixer.blend('auth.User', username='boss', is_staff=False)
    publisher1 = mixer.blend('auth.User', username='vasya', is_staff=False)
    obj3 = mixer.blend('posts.Post', pk=1, publish_date=timezone.now(), user=publisher1)
    obj2 = mixer.blend('posts.Post', pk=2, publish_date=timezone.now() + timedelta(days=30), user=publisher)
    obj1 = mixer.blend('posts.Post', pk=3, draft=True, user=publisher)
    return obj3, obj2, obj1, publisher


class TestPermissions:
    def test_is_owner_or_read_only(self, client, post_data):
        client.force_login(post_data[3])
        req = client.put(reverse('posts:api-detail', kwargs={'pk': 1}), data=json.dumps(form_data()))
        assert req.data['detail'] == 'You are not author of this post'
        req = client.put(reverse('posts:api-detail', kwargs={"pk": 2}), data=json.dumps(form_data()),
                         content_type="application/json")
        assert req.data['title'] == "some title"





















