from django.conf.urls import url

from posts.views import HomePage, PostView, ContactView, CreatePost, UpdatePost, DeletePost

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'post/(?P<pk>\d+)/$', PostView.as_view(), name='post'),
    url(r'contacts/$', ContactView.as_view(), name='contact'),
    url(r'post/create/$', CreatePost.as_view(), name='create'),
    url(r'post/update/(?P<pk>\d+)/$', UpdatePost.as_view(), name='update'),
    url(r'post/delete/(?P<pk>\d+)/$', DeletePost.as_view(), name='delete'),
]