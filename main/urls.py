from django.contrib.auth import views as auth_views
from django.urls import path

from main.views import CreateForumView, ForumView, IndexView, PostView, RegisterView

urlpatterns = [
    # anorum
    path("", IndexView.as_view(), name="index"),
    path("create/", CreateForumView.as_view(), name="create_forum"),
    path("a/<slug:forum_name>/", ForumView.as_view(), name="forum"),
    path("a/<slug:forum_name>/<int:parent_post_id>/", PostView.as_view(), name="post"),
    # accounts
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("register/", RegisterView.as_view(), name="register"),
]
