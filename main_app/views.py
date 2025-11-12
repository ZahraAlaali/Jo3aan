from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, User, Profile
from .forms import (
    CustomUserCreationForm,
    UpdateProfileForm,
    UpdateUserForm,
    CustomProfileCreationForm,
)

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    error_message = ""
    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        profile_form = CustomProfileCreationForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user_id = user.id
            profile.save()

            login(request, user)
            return redirect("/")
        else:
            error_message = "Invalid Sign Up, Try Again Later..."
    else:
        user_form = CustomUserCreationForm()
        profile_form = CustomProfileCreationForm()

    return render(
        request,
        "registration/signup.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "error_message": error_message,
        },
    )


def restaurants_index(request):
    restaurants = Restaurant.objects.all
    return render(request, "restaurants/index.html", {"restaurants": restaurants})


class RestaurantCreate(CreateView):
    model = Restaurant
    fields = "__all__"
    success_url = "/"


@login_required
def profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, "users/profile.html", {"profile": profile})


class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ["phone", "role", "profileImage"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def profile_user_update(request, user_id, profile_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method == "POST":
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UpdateUserForm(request.POST, instance=user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_data = profile_form.save()
            user_data = user_form.save()
            return redirect("/profile")
    else:
        profile_form = UpdateProfileForm(instance=profile)
        user_form = UpdateUserForm(instance=user)

    return render(
        request,
        "users/profile_user_update.html",
        {"profile_form": profile_form, "user_form": user_form},
    )
