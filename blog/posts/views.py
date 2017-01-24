from django.contrib import messages
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from posts.forms import EmailForm
from posts.models import Post


class HomePage(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/home.html'
    ordering = '-publish_date'

    def get_queryset(self):
        qs = self.model.objects.all()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q)|
                           Q(content__icontains=q)).distinct()
        qs = qs.order_by(self.get_ordering())
        return qs


class PostView(DetailView):
    template_name = 'posts/post.html'
    model = Post
    context_object_name = 'post'


class ContactView(TemplateView):
    template_name = 'posts/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data()
        context['form'] = EmailForm()
        return context

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            send_mail(form.cleaned_data['title'],
                      form.cleaned_data['message'],
                      'test@mail.ru',
                      [form.cleaned_data['email']])
            messages.add_message(request, messages.SUCCESS, 'Your message successfully sent.')
            return redirect('posts:contact')


class CreatePost(CreateView):
    model = Post
    template_name = 'posts/create.html'
    fields = ('title', 'content', 'image', 'draft')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instanse = form.save(commit=False)
            instanse.user = request.user
            instanse.save()
            return HttpResponseRedirect(instanse.get_absolute_url())
        context = {'form': form}
        return render(request, "posts/create.html", context)


class UpdatePost(UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    fields = ('title', 'content', 'image', 'draft')


class DeletePost(DeleteView):
    model = Post
    success_url = '/'


