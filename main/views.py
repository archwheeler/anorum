from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, ListView, TemplateView

from datetime import timedelta
from random import randrange

from main.forms import CustomUserCreationForm
from main.identities import IDENTITIES
from main.models import Forum, Post, UserIdentity

# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"


# TODO: refactor to use SuccessURLAllowedHostsMixin in Django 4.1
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

    def get_success_url(self):
        return self.get_redirect_url() or self.success_url

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get("next", self.request.GET.get("next"))
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.request.get_host(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""


class CreateForumView(LoginRequiredMixin, CreateView):
    model = Forum
    fields = ["name"]
    template_name = "main/create_forum.html"

    def form_valid(self, form):
        forum = form.save(commit=False)
        forum.owner = self.request.user
        forum.save()
        return HttpResponseRedirect(reverse_lazy("forum", args=[forum.name]))


class ForumView(ListView):
    template_name = "main/forum.html"

    def dispatch(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, name=self.kwargs["forum_name"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(
            forum=self.forum,
            parent__isnull=True,
            created_at__gte=timezone.now() - timedelta(days=1),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_name"] = self.kwargs["forum_name"]
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["body"]
    template_name = "main/create_post.html"

    def dispatch(self, request, *args, **kwargs):
        self.forum = get_object_or_404(Forum, name=self.kwargs["forum_name"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parent_post = form.save(commit=False)
        parent_post.forum = self.forum
        parent_post.owner = self.request.user

        identity_step_size = randrange(len(IDENTITIES))
        identity = IDENTITIES[identity_step_size]

        with transaction.atomic():
            parent_post.identity_step_size = identity_step_size
            parent_post.identity = IDENTITIES[identity_step_size]
            parent_post.identity_count = 1
            parent_post.save()

            user_identity = UserIdentity(
                user=self.request.user,
                identity=identity,
                parent_post=parent_post,
            )
            user_identity.save()

        return HttpResponseRedirect(reverse_lazy("post", args=[parent_post.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_name"] = self.kwargs["forum_name"]
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

        try:
            user_identity = UserIdentity.objects.get(
                user=self.request.user,
                parent_post=self.parent_post,
            )
        except UserIdentity.DoesNotExist:
            user_identity = None
            identity_creation_attempts = 0
            while user_identity is None and identity_creation_attempts < 3:
                try:
                    with transaction.atomic():
                        self.parent_post.identity_count += 1
                        self.parent_post.save()

                        if self.parent_post.identity_count <= len(IDENTITIES):
                            identity = IDENTITIES[
                                self.parent_post.identity_count
                                * self.parent_post.identity_step_size
                                % len(IDENTITIES)
                            ]
                        else:
                            identity = f"user #{self.parent_post.identity_count}"

                        user_identity = UserIdentity(
                            user=self.request.user,
                            identity=identity,
                            parent_post=self.parent_post,
                        )
                        user_identity.save()

                except IntegrityError:
                    self.parent_post.refresh_from_db()
                    user_identity = None

                identity_creation_attempts += 1

        if user_identity is None:
            form.add_error(None, "Error occurred while creating comment")
            return super().form_invalid(form)
        else:
            child_post.identity = user_identity.identity
            child_post.save()

        return HttpResponseRedirect(reverse_lazy("post", args=[self.parent_post.id]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_name"] = self.kwargs["forum_name"]
        context["parent_post"] = self.parent_post
        context["child_posts"] = Post.objects.filter(parent=self.parent_post)
        return context


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "registration/account.html"
