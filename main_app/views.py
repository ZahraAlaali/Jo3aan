from django.shortcuts import render, redirect
from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from .models import Restaurant
from .forms import CustomUserCreationForm

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/profile/create/")
        else:
            error_message = "Invalid Sign Up, Try Again Later..."

    form = CustomUserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


# def restaurants_index(request):
#     restaurants = Restaurant.objects.all
#     return render(request, "restaurants/index.html", {"restaurants": restaurants})


# class RestaurantCreate(CreateView):
#     model = Restaurant
#     fields = "__all__"
#     success_url = "/"
@login_required
def profile(request):
    return render(request, "users/profile.html")


class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ["phone", "role", "profileImage"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["phone", "role", "profileImage"]
