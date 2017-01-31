from django.http.response import HttpResponseForbidden


class MyPermissionMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user == self.get_object().user or \
                request.user.is_staff or request.user.is_superuser:
            return super(MyPermissionMixin, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You are not allowed to see this page!')