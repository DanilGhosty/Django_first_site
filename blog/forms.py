from django import forms
from .models import Post

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'post_img', 'text','post_slug')