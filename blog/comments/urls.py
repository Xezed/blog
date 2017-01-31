from django.conf.urls import url

from comments.views import CommentDetail, CommentDelete, CommentUpdate

urlpatterns = [
    url(r'(?P<pk>\d+)/$', CommentDetail.as_view(), name='comment'),
    url(r'(?P<pk>\d+)/delete/$', CommentDelete.as_view(), name='delete'),
    url(r'(?P<pk>\d+)/update/$', CommentUpdate.as_view(), name='update'),
]