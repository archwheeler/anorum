from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from main.forms import CustomUserCreationForm
from main.models import Forum, Post

# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")
    template_name = "registration/register.html"

    def form_valid(self, form):
        self.object = form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class CreateForumView(LoginRequiredMixin, CreateView):
    model = Forum
    fields = ["name"]
    template_name = "main/create_forum.html"

    def form_valid(self, form):
        forum = form.save(commit=False)
        forum.owner = self.request.user
        forum.save()
        return HttpResponseRedirect(reverse_lazy("forum", args=[forum.name]))


class ForumView(CreateView):
    model = Post
    fields = ["body"]
    template_name = "main/forum.html"

    def dispatch(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, name=self.kwargs["forum_name"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parent_post = form.save(commit=False)
        parent_post.forum = self.forum
        parent_post.owner = self.request.user
        parent_post.save()
        return HttpResponseRedirect(
            reverse_lazy("post", args=[self.forum.name, parent_post.id])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_name"] = self.kwargs["forum_name"]
        context["post_list"] = Post.objects.filter(
            forum=self.forum,
            parent__isnull=True,
        )
        return context


class PostView(CreateView):
    model = Post
    fields = ["body"]
    template_name = "main/post.html"

    def dispatch(self, request, *args, **kwargs):
        self.parent_post = get_object_or_404(Post, id=self.kwargs["parent_post_id"])
        if (
            self.parent_post.parent is not None
            or self.kwargs["forum_name"] != self.parent_post.forum.name
        ):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        child_post = form.save(commit=False)
        child_post.forum = self.parent_post.forum
        child_post.owner = self.request.user
        child_post.parent = self.parent_post
        child_post.save()
        return HttpResponseRedirect(
            reverse_lazy("post", args=[self.kwargs["forum_name"], self.parent_post.id])
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_name"] = self.kwargs["forum_name"]
        context["parent_post"] = self.parent_post
        context["child_posts"] = Post.objects.filter(parent=self.parent_post)
        return context
