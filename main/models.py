from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None

    def __str__(self):
        return self.username


class Forum(models.Model):
    name = models.SlugField(unique=True, max_length=32)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    body = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    identity = models.CharField(max_length=64)
    identity_step_size = models.IntegerField(null=True)
    identity_count = models.IntegerField(null=True)

    def __str__(self):
        return self.body


class UserIdentity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identity = models.CharField(max_length=64)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identity", "parent_post"], name="identity_unique_accross_post"
            )
        ]

    def __str__(self):
        return self.identity
