from django.conf.urls import url

from comments.api.views import CommentRUD, CommentCreate

urlpatterns = [
    url(r'(?P<pk>\d+)/$', CommentRUD.as_view(), name='comment-api'),
    url(r'create/$', CommentCreate.as_view(), name='create-api'),
    url(r'(?P<pk>\d+)/delete/$', CommentRUD.as_view(), name='delete-api'),
    url(r'(?P<pk>\d+)/update/$', CommentRUD.as_view(), name='update-api'),
]