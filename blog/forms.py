from dataclasses import fields
from django import forms
from .models import Post,Comment

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'post_img', 'text','post_slug')

class AddComment(forms.ModelForm):
    content = forms.CharField(label="Add Coment",widget=forms.Textarea(        
    attrs={'class':'form-control', 'rows':4, 'cols':50, 'placeholder':"Comment here..."}
    )) #label=" "
    class Meta:
        model = Comment
        fields = ['content']