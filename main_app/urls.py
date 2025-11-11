from django.urls import path, include
from . import views


urlpatterns = [
    # Sign Up
    path("accounts/signup/", views.signup, name="signup"),
    #
    path("", views.home, name="home"),
    # profile
    path("profile/", views.profile, name="profile"),
    # path("profile/create/", views.CreateProfile, name="craete_profile"),
]
