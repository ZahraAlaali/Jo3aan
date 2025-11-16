from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, Profile, CartDetails,Item


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class CustomProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "profileImage", "role"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "profileImage"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description","image", "price"]

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartDetails
        fields = ["quantity", "comment"]
