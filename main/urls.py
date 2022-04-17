from django.urls import include, path

from main.views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
