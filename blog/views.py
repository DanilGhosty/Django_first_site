from django.shortcuts import redirect, render, redirect
from django.http import  HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Post

# Create your views here.
def main_page(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by("published_date")
    else: posts = ""
    context={
        'posts': posts,
    }
    return render(request, 'main_page.html', context)

def register(request):
    form = UserCreationForm
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        pass
    context={'form':form}
    return render(request, 'register.html', context)

def logout_request(request):
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
                login(request,user)
                return redirect("/")
    form=AuthenticationForm()
    context={'form':form}
    return render(request, 'login.html', context)

