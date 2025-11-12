from django.urls import path, include
from . import views


urlpatterns = [
    # Sign Up
    path("accounts/signup/", views.signup, name="signup"),
    #
    path("", views.home, name="home"),
    path(
        "restaurants/create/",
        views.RestaurantCreate.as_view(),
        name="restaurant_create",
    ),
    path("restaurants/", views.restaurants_index, name="restaurants_index"),
    # profile
    path("profile/", views.profile, name="profile"),
    path("profile/create/", views.ProfileCreate.as_view(), name="craete_profile"),
    path(
        "profile/update/<int:user_id>/<int:profile_id>/",
        views.profile_user_update,
        name="profile_update",
    ),
    # Cart
    path("cart/add/<int:user_id>/", views.addToCart, name="addToCart"),
    path(
        "cart/changeStatus/<int:user_id>/<int:cart_id>/",
        views.changeCartStatus,
        name="changeCartStatus",
    ),  # change the status->place order
    path("cart/viewCart/<int:user_id>/", views.viewCart, name="viewCart"),
    path(
        "cartDetails/delete/<int:user_id>/<int:item_id>/",
        views.deleteItemFromCart,
        name="deleteItemFromCart",
    ),
]
