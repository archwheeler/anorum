from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from main.forms import CustomUserCreationForm

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
