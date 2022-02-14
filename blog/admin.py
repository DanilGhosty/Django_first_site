from django.contrib import admin
from .models import Post, Post_category,Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_category)
admin.site.register(Comment)