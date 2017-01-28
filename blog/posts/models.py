from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class PostManager(models.Manager):
    def published(self):
        qs = super(PostManager, self).filter(draft=False, publish_date__lte=timezone.now())
        return qs


class Post(models.Model):
    title = models.CharField(_('Title'), max_length=120)
    content = models.TextField(_('content'))
    draft = models.BooleanField(_('is draft?'), default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    publish_date = models.DateTimeField(_('publish date'), null=True, blank=True)
    change_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(_('image'), width_field='width_field', height_field='height_field')
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    objects = PostManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'pk': self.pk})
