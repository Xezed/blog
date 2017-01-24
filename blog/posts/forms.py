from django import forms


class EmailForm(forms.Form):
    title = forms.CharField(max_length=120)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)