import imp
from multiprocessing import context
from turtle import title
from unicodedata import category
from django.shortcuts import redirect, render, redirect
from django.http import  HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.defaults import page_not_found
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .models import Post, Post_category

# Create your views here.

def paginator(request, posts):
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)
    
    return posts_page

def main_page(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by("published_date")
        
    else: posts = ""
    categories = Post_category.objects.all()
    posts = paginator(request, list(posts))
    context={
        'posts': posts,
        'sidebar': categories
    }
    return render(request, 'main_page.html', context)


def search_post(request):
    posts = None
    if request.method == 'POST':
        searched= request.POST.get('searchpost')
        posts = Post.objects.filter(title__icontains=searched)
    sidebar = Post_category.objects.all()
    context = {'posts':posts,"sidebar":sidebar}
    
    return render(request, 'search_result.html',context)


def single_slug(request,single_slug):
    sidebar = Post_category.objects.all()
    categories = [cat.category_slug  for cat in Post_category.objects.all()]
    if single_slug in categories:
        category_posts = Post.objects.filter(post_category__category_slug=single_slug)
        return render(request, 'category.html', {'posts':category_posts,'sidebar': sidebar})
    posts_slug = [ p.post_slug for p in Post.objects.all()]
    if single_slug in posts_slug:
        post = Post.objects.get(post_slug=single_slug)
        context = {"post": post,'sidebar': sidebar}
        return render(request, 'post_view.html', context)
    
    #post_slug =[p.post_slug for p in Post.objects.all() ]
    #if single_slug in post_slug:
    #    post = Post.objects.get(post_slug = single_slug)
    #    context = {"post": post}
    #    return render(request, 'post_view.html', context)
    else:
        raise Http404
        #page_not_found(request, 'Articule not founde')
        
        

def register(request):    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"You created your account: {username}")
            login(request, user)
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request,f'{msg} : {form.error_messages[msg]}')
            return render(request, 'register.html', context={'form':form})
    form = UserCreationForm
    context={'form':form}
    return render(request, 'register.html', context)

def logout_request(request):
    messages.success(request,"You secssesfully leave your account")
    logout(request)
    return redirect("/")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                messages.success(request,f"You secssesfully enterred your account: {username}")
                login(request,user)
                return redirect("/")
    form=AuthenticationForm()
    context={'form':form}
    return render(request, 'login.html', context)

