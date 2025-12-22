from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Topic, Comment
from openai import OpenAI, OpenAIError
from django.contrib.auth.decorators import login_required
import json


client = OpenAI()




@login_required(login_url="signin")
def postcomment(request, id):
    if request.method != "POST":
        return redirect("topic_detail", id=id)

    topic = get_object_or_404(Topic, id=id)
    text = (request.POST.get("text") or "").strip()

    if not text:
        messages.error(request, "Comment cannot be empty.")
        return redirect("topic_detail", id=id)

    # Defaults (in case calls fail)
    categories = {}
    scores = {}
    flagged = False
    top_label = "unknown"

    has_profanity = False
    profanity_severity = "none"  # none|mild|strong

    # 1) Moderation API
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=text,
        )
        result = response.results[0]

        categories = dict(result.categories)
        scores = dict(result.category_scores)
        flagged = bool(result.flagged)

        flagged_labels = [k for k, v in categories.items() if v]
        top_label = "clean"
        if flagged_labels:
            top_label = max(flagged_labels, key=lambda k: scores.get(k, 0))

    except OpenAIError:
        messages.warning(request, "Moderation service unavailable. Comment posted without moderation label.")

    # 2) Profanity classification (OpenAI model call)
    try:
        prof_resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a profanity detector for forum comments in any language. "
                        "Return ONLY valid JSON with exactly these keys: "
                        "{\"has_profanity\": boolean, "
                        "\"severity\": \"none\"|\"mild\"|\"strong\"}. "
                        "Do not include any other text."
                    ),
                },
                {"role": "user", "content": text},
            ],
        )

        raw = (prof_resp.output_text or "").strip()
        data = json.loads(raw)

        has_profanity = bool(data.get("has_profanity", False))
        profanity_severity = data.get("severity", "none")
        if profanity_severity not in ("none", "mild", "strong"):
            profanity_severity = "none"

    except (OpenAIError, json.JSONDecodeError):
        # don't block comment posting if classifier fails
        messages.warning(request, "Profanity classifier unavailable. Comment posted without profanity label.")

    Comment.objects.create(
        topic=topic,
        user=request.user,
        text=text,
        is_flagged=flagged,
        labels=categories,
        scores=scores,
        top_label=top_label,
        has_profanity=has_profanity,
        profanity_severity=profanity_severity,
    )

    return redirect("topic_detail", id=id)



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
