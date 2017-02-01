from datetime import timedelta

import pytest
from django.test.client import Client
from django.utils import timezone
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db


class TestHomePageView:
    def test_anonymous(self):
        obj = mixer.blend('posts.Post', title='abc', publish_date=timezone.now())
        obj2 = mixer.blend('posts.Post', title='abb', publish_date=timezone.now())
        obj3 = mixer.blend('posts.Post', title='bbb', publish_date=timezone.now())
        obj1 = mixer.blend('posts.Post', draft=True)
        req = Client().get('/')
        assert req.status_code == 200
        assert obj in req.context['posts']
        assert obj1 not in req.context['posts']
        req = Client().get('/?q=test')
        assert req.context['posts'].count() == 0
        req = Client().get('/?q=ab')
        assert obj, obj2 in req.context['posts']
        assert obj3, obj1 not in req.context['posts']
        assert obj3, obj1 not in req.context['posts']


class TestPostView:
    def test_authorization(self):
        user = Client()
        publisher = mixer.blend('auth.User', username='boss')
        obj3 = mixer.blend('posts.Post', pk=1, publish_date=timezone.now(), user=publisher)
        obj3 = mixer.blend('posts.Post', pk=2, publish_date=timezone.now()+timedelta(days=30), user=publisher)
        obj1 = mixer.blend('posts.Post', pk=3, draft=True, user=publisher)
        admin_mod = mixer.blend('auth.User', password='awesome1', username='abc', is_staff=True)
        admin_mod.set_password('awesome1')
        admin_mod.save()
        admin = Client()
        admin.login(password='awesome1', username='abc')
        res = user.get('/post/1/')
        assert res.status_code == 200
        res = user.get('/post/2/')
        assert res.status_code == 403
        res = user.get('/post/3/')
        assert res.status_code == 403
        res = admin.get('/post/1/')
        assert res.status_code == 200
        res = admin.get('/post/2/')
        assert res.status_code == 200
        res = admin.get('/post/3/')
        assert res.status_code == 200
        user.force_login(publisher)
        res = user.get('/post/1/')
        assert res.status_code == 200
        res = user.get('/post/2/')
        assert res.status_code == 200
        res = user.get('/post/3/')
        assert res.status_code == 200
