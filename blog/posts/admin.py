from django.contrib import admin

from posts.models import Post


class AdminPost(admin.ModelAdmin):
    ordering = ['-publish_date', 'title']
    list_filter = ['publish_date',]
    list_display = ['title', 'publish_date', 'user']


admin.site.register(Post, AdminPost)