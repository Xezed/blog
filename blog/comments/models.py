from django.contrib.auth.models import User
from django.db import models

from posts.models import Post


class CommentManager(models.Manager):
    def parents(self):
        return super(CommentManager, self).filter(parent_comment=None)


class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(Post)
    parent_comment = models.ForeignKey('self', null=True, blank=True)

    objects = CommentManager()

    def __str__(self):
        return str(self.content)

    @property
    def has_children(self):
        if self.parent_comment:
            return False
        else:
            return True

    def children(self):
        return Comment.objects.filter(parent_comment=self)
