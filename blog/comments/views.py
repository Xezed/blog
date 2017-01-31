from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, DeleteView, UpdateView

from comments.forms import CommentForm
from comments.models import Comment
from posts.mixins import MyPermissionMixin


class CommentDetail(FormView, DetailView):
    context_object_name = 'comment'
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment.html'


class CommentDelete(MyPermissionMixin, DeleteView):
    model = Comment
    success_message = _('Comment successfully deleted')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CommentDelete, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.get_object().parent.get_absolute_url()


class CommentUpdate(MyPermissionMixin, SuccessMessageMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    success_message = _('Comment successfully updated')
    template_name = 'comments/comment_update.html'

    def get_success_url(self):
        return self.get_object().parent.get_absolute_url()

