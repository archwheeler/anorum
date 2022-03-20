from django.http import HttpResponse
from django.shortcuts import render
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
    response = "post %s"
    return HttpResponse(response % post_id)
