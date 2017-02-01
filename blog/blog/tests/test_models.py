import pytest
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from mixer.backend.django import mixer

from comments.models import Comment
from posts.models import Post

pytestmark = pytest.mark.django_db


class TestPost:
    def test_init(self):
        obj = mixer.blend('posts.Post', title='Some test')
        assert obj.pk == 1, 'Should save an instance'
        obj.__str__() == 'Some test', 'Return correct representation'
        assert '/post/' + str(obj.pk) + '/' == obj.get_absolute_url()

    def test_post_manager(self):
        obj_draft = mixer.blend('posts.Post', draft=True)
        obj_future = mixer.blend('posts.Post', publish_date=timezone.now()+timedelta(days=30))
        obj_past = mixer.blend('posts.Post', draft=False, publish_date=timezone.now()+timedelta(days=-30))
        user = AnonymousUser()
        assert Post.objects.published(user=user).count() == 1
        user_admin = mixer.blend('auth.User', is_staff=True)
        assert Post.objects.published(user=user_admin).count() == 3


class TestComment:
    def test_comment_manager(self):
        obj = mixer.blend('comments.Comment', parent_comment=None, content='abc')
        child_obj = mixer.blend('comments.Comment', parent_comment=obj)
        assert Comment.objects.parents().count() == 1
        assert 'abc' == obj.__str__()

    def test_comment_methods(self):
        obj = mixer.blend('comments.Comment', parent_comment=None, pk=1)
        obj2 = mixer.blend('comments.Comment', parent_comment=None)
        obj3 = mixer.blend('comments.Comment', parent_comment=None)
        child_obj = mixer.blend('comments.Comment', parent_comment=obj)
        child_obj2 = mixer.blend('comments.Comment', parent_comment=obj2)
        child_obj3 = mixer.blend('comments.Comment', parent_comment=obj2)
        assert obj.has_children is True
        assert child_obj.has_children is False
        assert obj3.has_children is False
        assert obj2.children().count() == 2
        assert obj.children().count() == 1
        assert obj.get_absolute_url() == '/comments/' + str(obj.pk) + '/'

















