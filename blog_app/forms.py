from django import forms
from .models import Comment, Post


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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "body",
        )
