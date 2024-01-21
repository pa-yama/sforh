from django import forms
from ..models import Post_Tmp, Post, Comment, Reaction

class SearchPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
                    "title",
                 ]