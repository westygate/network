
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    
    #API
    path("new_post", views.new_post, name="new_post"),
    path("posts/<str:category>/<int:page>", views.view_posts, name="view_posts"),
    path("post/<int:id>", views.update_post, name="update_post"),
    path("like/<int:id>", views.like_post, name="like_post"),
    path("user/<int:id>", views.user_profile, name="user_profile"),
    path("follow/<int:id>", views.follow_user, name="follow_user")
    
]
