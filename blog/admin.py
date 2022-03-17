from re import A
from django.contrib import admin

from .models import Post, Post_category,Comment,Profile
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_category)
admin.site.register(Comment)
admin.site.register(Profile)