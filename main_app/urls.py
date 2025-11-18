from django.urls import path, include
from . import views

from .views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Sign Up
    path("accounts/signup/", views.signup, name="signup"),
    #
    path("", views.home, name="home"),
    # profile
    path("profile/", views.profile, name="profile"),
    path("profile/create/", views.ProfileCreate.as_view(), name="craete_profile"),
    path(
        "profile/update/<int:user_id>/<int:profile_id>/",
        views.profile_user_update,
        name="profile_update",
    ),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="main_app/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="main_app/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # Restaurant
    path("restaurants/", views.restaurants_index, name="restaurants_index"),
    path(
        "restaurants/<int:restaurant_id>/",
        views.restaurant_details,
        name="restaurant_details",
    ),
    path(
        "restaurants/create/",
        views.RestaurantCreate.as_view(),
        name="restaurant_create",
    ),
    path(
        "restaurants/<int:pk>/update/",
        views.RestaurantUpdate.as_view(),
        name="restaurant_update",
    ),
    path(
        "restaurants/<int:pk>/delete/",
        views.RestaurantDelete.as_view(),
        name="restaurant_delete",
    ),
    # item
    # path("item/<int:pk>/", views.ItemDetail.as_view(), name="item_detail"),
    # path("item/create/", views.ItemCreat.as_view(), name="item_create"),
    path("item/<int:pk>/update/", views.ItemUpdate.as_view(), name="item_update"),
    path("item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item_delete"),
    path("restaurants/<int:restaurant_id>/add_item", views.add_item, name="add_item"),
    # Cart
    path(
        "cart/add/<int:user_id>/<int:item_id>/<int:restaurant_id>/",
        views.addToCart,
        name="addToCart",
    ),
    path("cart/viewCart/<int:user_id>/", views.viewCart, name="viewCart"),
    path(
        "cartDetails/delete/<int:user_id>/<int:cartDetail_id>/",
        views.deleteItemFromCart,
        name="deleteItemFromCart",
    ),
    path(
        "cartDetails/update/<int:user_id>/<int:cartDetail_id>/inc/",
        views.increaseQty,
        name="increaseQty",
    ),
    path(
        "cartDetails/update/<int:user_id>/<int:cartDetail_id>/dec/",
        views.decreaseQty,
        name="decreaseQty",
    ),
    path(
        "cart/createNewCart/<int:user_id>/<int:item_id>/<int:restaurant_id>/",
        views.createNewCart,
        name="createNewCart",
    ),
    path("orders/create/<int:user_id>/", views.createOrder, name="create_order"),
    path(
        "orders/customer/<int:user_id>/", views.customerOrders, name="customer_orders"
    ),
    path("orders/restaurant/", views.restaurantOrders, name="restaurant_orders"),
    path("orders/ready/<int:order_id>/", views.mark_order_ready, name="mark_ready"),
    path('orders/driver/',views.driver_orders.as_view(), name='driver_orders')

]
