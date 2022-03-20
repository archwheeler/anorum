from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Post

# Create your views here.
def index(request):
    latest_posts_list = Post.objects.order_by("-created_at")[:5]
    template = loader.get_template("posts/index.html")
    context = {
        "latest_posts_list": latest_posts_list,
    }
    return render(request, "posts/index.html", context)


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "posts/post.html", {"post": post})
