from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.views.generic.list import ListView

from comments.forms import CommentForm
from comments.models import Comment
from posts.forms import EmailForm, PostForm
from posts.mixins import MyPermissionMixin
from posts.models import Post


class HomePage(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/home.html'
    ordering = '-publish_date'

    def get_queryset(self):
        qs = self.model.objects.published(self.request.user)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(content__icontains=q)).distinct()
        qs = qs.order_by(self.get_ordering())
        return qs


class PostView(FormMixin, DetailView):
    template_name = 'posts/post.html'
    model = Post
    form_class = CommentForm
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        user = self.request.user if self.request.user.is_authenticated else None
        if self.model.objects.filter(~Q(user=user),
                                     id=kwargs['pk'], draft=True) and not self.request.user.is_staff:
            return HttpResponseForbidden('Forbidden')
        else:
            return super(PostView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            post = request.POST.get('post_id')
            comment = request.POST.get('comment_id')
            if comment:
                comment = Comment.objects.get(id=comment)

            instance = form.save(commit=False)
            instance.parent_comment = comment
            instance.user = request.user
            instance.parent = Post.objects.get(id=post)
            instance.save()
            messages.success(request, _('Comment created'))
            return HttpResponseRedirect(instance.parent.get_absolute_url())


class ContactView(FormView):
    template_name = 'posts/contact.html'
    form_class = EmailForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            send_mail(form.cleaned_data['title'],
                      form.cleaned_data['message'],
                      'test@mail.ru',
                      [form.cleaned_data['email']])
            messages.success(request, _('Your message successfully sent.'))
            return redirect('posts:contact')


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {'form': form}
        return render(request, "posts/create.html", context)


class UpdatePost(MyPermissionMixin, UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    form_class = PostForm


class DeletePost(MyPermissionMixin, DeleteView):
    model = Post
    success_message = _('Post successfully deleted')
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeletePost, self).delete(request, *args, **kwargs)
