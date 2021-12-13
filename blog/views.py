from django.shortcuts import render
from django.http import  HttpResponse
from .models import Post
# Create your views here.
def main_page(request):
    posts = Post.objects.all().order_by("published_date")
    context={
        'posts': posts,
    }
    return render(request, 'main_page.html', context)