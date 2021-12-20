from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        labels = {
            "body": "",
        }


class SearchForm(forms.Form):
    search = forms.CharField()
