from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }
    
    def get_followed_users(self):
        followed_users = [followed_user.user for followed_user in
                          Followers.objects.filter(follower=self)]
        return followed_users
    
    def get_followers_list(self):
        followers = Followers.objects.filter(user=self);
        followers_list = [follower.follower for follower in followers]
        return followers_list
    
    def get_followers_list_json(self):
        followers = Followers.objects.filter(user=self);
        followers_json = [follower.follower.serialize() for follower in followers]
        return followers_json
    
    def get_posts(self):
        posts = Post.objects.filter(owner=self)
        posts_list = [post.serialize() for post in posts]
        return posts_list
    
        
    def full_info_serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": self.get_followers_list_json(),
            "posts": self.get_posts()
        }
    

class Post(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    timestamp = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(User, blank=True)
    
    def like_users_to_list(self):
        like_users_list = [user.serialize() for user in self.like_users.all()]
        return like_users_list
    
    def likes_count(self):
        return self.like_users.count()
    
    
    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.serialize(),
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes_count(),
            "like_users": self.like_users_to_list()
        }
    
    class Meta:
        ordering = ["timestamp"]
    
    
 

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_person")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_is_follower")

