from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_protect

from .forms import SignUpForm, SignInForm


@csrf_protect
def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            messages.error(request, "Invalid credentials.")
            return render(request, "login.html", {"form": form})
        else:
            login(request, user)
            return redirect("/")
    else:
        form = SignInForm()
    return render(request, "login.html", {"form": form})


@csrf_protect
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Please make sure captcha is filled!")
            return render(request, "signup.html", {"form": form})
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = (
        "first_name",
        "last_name",
        "email",
    )
    template_name = "my_account.html"
    success_url = reverse_lazy("my_account")

    def get_object(self):
        return self.request.user
