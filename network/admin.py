from django.contrib import admin

# Register your models here.
from .models import User, Post, Followers

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Followers)