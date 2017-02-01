from django.test import TestCase
from django.utils import timezone

from posts.models import Post
from posts.utils import random_word


class PostTestCase(TestCase):
    def setUp(self):
        user1 = User
    def test_create_post(self):
        post = Post.objects.create(
            title=random_word(10), content=random_word(400), publish_date=timezone.now()
        )

        response = self.client.get(post.get_absolute_url())
        self.assertEqual(response.status_code, 200)




