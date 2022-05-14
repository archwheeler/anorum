from django.contrib.auth import views as auth_views
from django.urls import path

from main.views import (
    CreateForumView,
    CreatePostView,
    ForumView,
    IndexView,
    PostView,
    RegisterView,
)

urlpatterns = [
    # anorum
    path("", ForumView.as_view(), {"forum_name": "anorum"}, name="index"),
    path(
        "post/", CreatePostView.as_view(), {"forum_name": "anorum"}, name="create_post"
    ),
    path(
        "post/<int:parent_post_id>/",
        PostView.as_view(),
        {"forum_name": "anorum"},
        name="post",
    ),
    # path("create/", CreateForumView.as_view(), name="create_forum"),
    # path("a/<slug:forum_name>/", ForumView.as_view(), name="forum"),
    # path("a/<slug:forum_name>/post/", CreatePostView.as_view(), name="create_post"),
    # path(
    #     "a/<slug:forum_name>/post/<int:parent_post_id>/",
    #     PostView.as_view(),
    #     name="post",
    # ),
    # accounts
    path(
        "login/",
        auth_views.LoginView.as_view(),
        {"hide_navbar_account": True},
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        {"hide_navbar_account": True},
        name="logout",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        {"hide_navbar_account": True},
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        {"hide_navbar_account": True},
        name="password_change_done",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        {"hide_navbar_account": True},
        name="register",
    ),
]
