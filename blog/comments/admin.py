from django.contrib import admin

from comments.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'pub_date', 'change_date')
    search_fields = ('content',)
    list_filter = ('change_date',)

admin.site.register(Comment, CommentAdmin)