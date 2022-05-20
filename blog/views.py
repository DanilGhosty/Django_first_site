from multiprocessing import context
from turtle import title
from django.shortcuts import redirect, render, get_list_or_404
from django.http import  HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.defaults import page_not_found
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.urls import reverse
from .forms import AddPostForm,AddComment, UpdateProfileform, \
    UpdateUserForm, RegisterForm
from .models import Post, Post_category, Comment, Profile
from django.contrib.auth.decorators import login_required
from chat.views import unread_msg_num


# Create your views here.

def LikeView(request, pk):
    post= get_list_or_404(Post,post_slug=request.POST.get('post_slug'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_view',args=[str(pk)]))


def paginator(request, posts):
    paginator = Paginator(posts, 2)
    if request.method == 'POST':
        page = request.POST.get('page')
    else :
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
    msg_num = unread_msg_num(request)
    context={
        'posts': posts,
        'sidebar': categories,
        'msg_num': msg_num
    }
    return render(request, 'main_page.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileform(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(to='user_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileform(instance=request.user.profile)
    profile = request.user.profile
    context = {
        'profile': profile,
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request, 'profile.html', context)

def look_profile(request,profile):
    profile = Profile.objects.get(user__username=profile)
    if profile == request.user.profile:
        return redirect(to='user_profile')
    return render(request, 'look_profile.html',
                 {'profile': profile}
                  )
    


def add_post(request):
    add_post_form=None
    if request.user.is_authenticated:
        if request.method == "POST":
            add_post_form = AddPostForm(request.POST, request.FILES)
            if add_post_form.is_valid():
                url = request.POST.get('post_slug')
                new_post = add_post_form.save()
                new_post.save()
                print(url)
                return redirect(f"/{url}")
            else:
                print("unValid")
        else:
            add_post_form = AddPostForm()
    context={
        'post_form':add_post_form,
    }        
    return render(request,'add_post.html', context)

def search_post(request):
    posts = None
    if request.method == 'POST':
        searched= request.POST.get('searchpost')
        posts = Post.objects.filter(title__icontains=searched)
        posts = paginator(request, list(posts))
    sidebar = Post_category.objects.all()
 
    context = {'posts':posts,"sidebar":sidebar}
    
    return render(request, 'search_result.html',context)

def post_comment(request, post):
    if request.method == 'POST':
        form = AddComment(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post = post,author = request.user, content = content)
            comment.save()
            return redirect(f'/{post.post_slug}')
        else:
            return redirect(f'/{post.post_slug}')
    else:
        form = AddComment()
        return form

def single_slug(request,single_slug):
    sidebar = Post_category.objects.all()
    categories = [cat.category_slug  for cat in Post_category.objects.all()]
    if single_slug in categories:
        category_posts = Post.objects.filter(post_category__category_slug=single_slug)
        return render(request, 'category.html', {'posts':category_posts,'sidebar': sidebar})
    posts_slug = [ p.post_slug for p in Post.objects.all()]
    if single_slug in posts_slug:
        posts = Post.objects.get(post_slug=single_slug)
        comments = Comment.objects.filter(post = posts)
        form = post_comment(request, posts)
        context = {"post": posts,'sidebar': sidebar,'comment_form':form,'comments':comments}
        return render(request, 'post_view.html', context)
    else:
        return Http404
    
    #post_slug =[p.post_slug for p in Post.objects.all() ]
    #if single_slug in post_slug:
    #    post = Post.objects.get(post_slug = single_slug)
    #    context = {"post": post}
    #    return render(request, 'post_view.html', context)
    #else:
    #    raise Http404
        #page_not_found(request, 'Articule not founde')               

def register(request):    
    if request.method == "POST":
        form = RegisterForm(request.POST)
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
    form = RegisterForm
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

