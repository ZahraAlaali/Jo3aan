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
    path("profile/create/", views.ProfileCreate.as_view(), name="create_profile"),
    # item
    path("item/", views.ItemList.as_view(), name="item_list"),
    path("item/<int:pk>/", views.ItemDetail.as_view(), name="item_detail"),
    path("item/create/", views.ItemCreate.as_view(), name="item_create"),
    path("item/<int:pk>/update/", views.ItemUpdate.as_view(), name="item_update"),
    path("item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item_delete"),
    path(
        "profile/update/<int:user_id>/<int:profile_id>/",
        views.profile_user_update,
        name="profile_update",
    ),
    path(
        "restaurants/<int:restaurant_id>/",
        views.restaurant_details,
        name="restaurant_details",
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
    # Cart
    path("cart/add/<int:user_id>/<int:item_id>/<int:restaurant_id>/", views.addToCart, name="addToCart"),
    path(
        "cart/changeStatus/<int:user_id>/<int:cart_id>/",
        views.changeCartStatus,
        name="changeCartStatus",
    ),  # change the status->place order
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
        "orders/create/<int:user_id>/",
        views.createOrder,
        name="create_order"
    ),
]
