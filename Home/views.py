from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Topic, Comment

def postcomment(request, id):
    return None

def topic(request, id):
    topic = get_object_or_404(Topic, id=id)
    comments = Comment.objects.filter(topic=topic).order_by("-created_at")

    return render(request, "Home/details.html", {
        "topic": topic,
        "comments": comments
    })

def index(request):
    topics = Topic.objects.order_by("-created_at")  # newest first
    return render(request, "Home/index.html", {
        "topics": topics
    })


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect("home")   

    return render(request, "Home/signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")   
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "Home/login.html")


def signout(request):
    auth_logout(request)          
    return redirect("home")       
