from django.urls import path, include
from . import views


urlpatterns = [
    # Sign Up
    path("accounts/signup/", views.signup, name="signup"),
    #
    path("", views.home, name="home"),
    # path('restaurants/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    # path('restaurants/',views.restaurants_index, name='restaurants_index'),
    path("profile/", views.profile, name="profile"),
    path("profile/create/", views.ProfileCreate.as_view(), name="craete_profile"),
]
