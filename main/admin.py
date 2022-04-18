from django.contrib import admin
from main.models import Forum, Post, User

# Register your models here.
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(User)
