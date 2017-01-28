from django import forms
from django.forms.widgets import SelectDateWidget
from pagedown.widgets import PagedownWidget

from posts.models import Post


class EmailForm(forms.Form):
    title = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    publish_date = forms.DateTimeField(widget=SelectDateWidget())

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'publish_date', 'draft')
