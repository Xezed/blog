from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse
from django.utils import timezone


class PostManager(models.Manager):
    def published(self):
        qs = super(PostManager, self).filter(draft=False, publish_date__lte=timezone.now())
        return qs

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(null=True, blank=True)
    change_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(width_field='width_field', height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'pk':self.pk})


