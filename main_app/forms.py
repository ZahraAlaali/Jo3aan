from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "profileImage"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
