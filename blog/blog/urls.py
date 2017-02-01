from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from blog.views import ProfileView
from posts import urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^api/comments/', include('comments.api.urls', namespace='comments-api')),
    url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^', include(urls, namespace='posts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

