from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from posts.models import Post


class AdminPost(admin.ModelAdmin):
    ordering = ['-publish_date', 'title']
    list_filter = ['publish_date']
    list_display = ['title', 'publish_date', 'user']

    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


admin.site.register(Post, AdminPost)
admin.site.site_header = 'Blog'
