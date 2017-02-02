from datetime import timedelta

import pytest
from django.core import mail
from django.test.client import Client, RequestFactory
from django.utils import timezone
from mixer.backend.django import mixer

from comments.models import Comment
from posts.models import Post
from posts.views import CreatePost

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


@pytest.fixture()
def form_data():
    data = {'title': 'some title', 'content': 'asd7',
            'publish_date_year': 2017, 'publish_date_month': 2, 'publish_date_day': 1}
    return data

@pytest.fixture()
def post_data():
    publisher = mixer.blend('auth.User', username='boss', is_staff=False)
    obj3 = mixer.blend('posts.Post', pk=1, publish_date=timezone.now(), user=publisher)
    obj2 = mixer.blend('posts.Post', pk=2, publish_date=timezone.now() + timedelta(days=30), user=publisher)
    obj1 = mixer.blend('posts.Post', pk=3, draft=True, user=publisher)
    return obj3, obj2, obj1, publisher

@pytest.fixture()
def comment_data():
    data = {'content': 'Some content', 'post_id': 1}
    child_data = {'content': 'cont', 'post_id': 1, 'comment_id': 2}
    child_data2 = {'content': 'conten', 'post_id': 1, 'comment_id': 3}
    return data, child_data, child_data2


class TestPostView:
    def test_authorization(self):
        user = Client()
        publisher = mixer.blend('auth.User', username='boss', is_staff=False)
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

    def test_create_post(self, client, data=form_data()):
        res = client.post('/post/create/', data=data)
        assert res.status_code == 302
        assert '/login/' in res.url
        user = mixer.blend('auth.User', username='abc')
        client.force_login(user)
        res = client.post('/post/create/', data=data)
        assert res.status_code == 302
        post = Post.objects.all()
        assert post.count() == 1
        assert res.url == post.first().get_absolute_url()
        res = client.post('/post/create/')
        assert res.status_code == 200
        assert bool(res.context['form'].errors) is True

    def test_delete_post(self, client, post_data):
        res = client.post('/post/delete/1/')
        assert res.status_code == 403
        posts = Post.objects.all()
        assert posts.count() == 3
        client.force_login(post_data[3])
        res = client.post('/post/delete/1/')
        assert res.status_code == 302
        assert posts.count() == 2

    def test_view_post(self, client, admin_client, post_data, comment_data):
        mixer.blend('comments.Comment', pk=2, parent=post_data[0])
        mixer.blend('comments.Comment', pk=3, parent=post_data[1])
        client.force_login(post_data[3])
        comments = Comment.objects.all()
        assert comments.count() == 2
        res = client.post('/post/1/', data=comment_data[0])
        assert comments.count() == 3
        assert res.url == '/post/1/'
        assert client.post('/post/1/', data=comment_data[1])
        assert comments.count() == 4
        assert client.post('/post/1/', data=comment_data[2])
        assert comments.count() == 4


class TestContactView:
    def test_contact_view(self, client):
        client.post('/contacts/', data={'title': 'Hello',
                                        'message': 'Wuzzup',
                                        'email': 'abc@gmail.com'})
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ['abc@gmail.com']


class TestCommentViews:
    def test_comment_delete(self, client, post_data):
        mixer.blend('comments.Comment', pk=2, parent=post_data[0], user=post_data[3])
        mixer.blend('comments.Comment', pk=3, parent=post_data[0])
        client.force_login(post_data[3])
        comments = Comment.objects.all()
        assert comments.count() == 2
        res = client.post('/comments/2/delete/')
        assert res.url == post_data[0].get_absolute_url()
        assert comments.count() == 1
        res = client.post('/comments/3/delete/')
        assert res.status_code == 403
        assert comments.count() == 1

    def test_comment_update(self, client, post_data):
        comment = mixer.blend('comments.Comment', pk=2, parent=post_data[0], user=post_data[3])
        client.force_login(post_data[3])
        res = client.post('/comments/2/update/', data={'content': 'updated'})
        comment.refresh_from_db()
        assert comment.content == 'updated'
        assert res.url == comment.parent.get_absolute_url()
