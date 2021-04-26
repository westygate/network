from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import datetime
from django.core import serializers
from django.core.paginator import Paginator

from .models import User, Post, Followers



def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    data = json.loads(request.body)
    text = data.get("text")
    new_post = Post(text=text, owner=request.user)
    new_post.save()
    return JsonResponse({"success": "Post saved successully"}, status=201)


def view_posts(request, category, page):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required"}, status=400)
    
    posts=[]

    if category == "all":
        posts = Post.objects.all()
    if category == "following":
        followed_users = request.user.get_followed_users()
        posts = Post.objects.filter(owner__in = followed_users)
        
    paginator = Paginator(posts, 2)
    page_obj = paginator.get_page(page)
    return JsonResponse({"posts": [post.serialize() for post in page_obj],
                         "page_count": paginator.num_pages,
                         "user": request.user.id}, safe=False)    
    

def user_profile(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required"}, status=400)
    user=User.objects.get(id=id)
    followers_list = user.get_followers_list()
    if user == request.user or not request.user.is_authenticated:
        follow = "none"
    elif request.user in followers_list:
        follow = "unfollow"
    elif request.user not in followers_list:
        follow = "follow"

    return JsonResponse({"profile": user.full_info_serialize(),
                         "follow": follow,
                         "current_user": request.user.id})


@csrf_exempt
@login_required(login_url='login')
def follow_user(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    
    followed_user = User.objects.get(id=id)
    data = json.loads(request.body)
    if data.get("follow") == "follow":
        new_follow = Followers.objects.create(user=followed_user, follower=request.user)
        return JsonResponse({"message": "Success following"}, status=201)
    if data.get("follow") == "unfollow":
        old_follow = Followers.objects.filter(user=followed_user, follower=request.user)
        old_follow.delete()
        return JsonResponse({"message": "Success unfollowing"}, status=201)
    
    
@csrf_exempt
@login_required(login_url='/login/')    
def update_post(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    
    post = Post.objects.get(id=id)
    if post.owner == request.user:
        data = json.loads(request.body)
        text = data.get("text")
        post.text = text
        post.save()
        return JsonResponse({"Success":"Post updated"}, status=201)
    else:
        return JsonResponse({"error":"You are not an owner"}, status=400)
  
    
@csrf_exempt
@login_required(login_url='/login/')
def like_post(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    
    post = Post.objects.get(id=id)
    if json.loads(request.body).get("like"):
        post.like_users.add(request.user)
        post.save()
        return JsonResponse({"message":"Post liked"}, status=201)
    else:
        post.like_users.remove(request.user)
        post.save()
        return JsonResponse({"message":"Post unliked"}, status=201)