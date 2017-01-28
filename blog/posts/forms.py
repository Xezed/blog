from django import forms
from django.forms.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from pagedown.widgets import PagedownWidget

from posts.models import Post


class EmailForm(forms.Form):
    title = forms.CharField(label=_('Title'), max_length=120)
    email = forms.EmailField(label=_('Email'))
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)


class PostForm(forms.ModelForm):
    content = forms.CharField(label=_('Content'), widget=PagedownWidget())
    publish_date = forms.DateTimeField(label=_('Publish date'), widget=SelectDateWidget())

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'publish_date', 'draft')
