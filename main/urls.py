from django.contrib.auth import views as auth_views
from django.urls import path

from main.views import IndexView

urlpatterns = [
    # anorum
    path("", IndexView.as_view(), name="index"),
    # accounts
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
