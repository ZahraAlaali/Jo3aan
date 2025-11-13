from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, User, Profile, Cart, CartDetails, Item
from .forms import (
    CustomUserCreationForm,
    UpdateProfileForm,
    UpdateUserForm,
    CustomProfileCreationForm,
)
import datetime
from django import forms
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

# restaurant part
@login_required
def restaurants_index(request):
    owner_restaurants = Restaurant.objects.filter(user=request.user)
    customer_restaurants = Restaurant.objects.all()
    now = datetime.datetime.now().time()
    print(request.user.profile.role)
    if request.user.profile.role=='owner':
        restaurants=owner_restaurants
    else:
        restaurants=customer_restaurants
    def checkTime():
        for restaurant in customer_restaurants:
            if restaurant.close_at< restaurant.open_at:
                restaurant.is_open=now>=restaurant.open_at or now<=restaurant.close_at
            else:
                restaurant.is_open =restaurant.open_at <= now < restaurant.close_at
        for restaurant in owner_restaurants:
            if restaurant.close_at< restaurant.open_at:
                restaurant.is_open=now>=restaurant.open_at or now<=restaurant.close_at
            else:
                restaurant.is_open =restaurant.open_at <= now < restaurant.close_at
    checkTime()
    return render(
        request, "restaurants/index.html", {'restaurants':restaurants, "now": now}
    )


class RestaurantCreate(LoginRequiredMixin,CreateView):
    model = Restaurant
    fields = ['name','description','image','city','categories','close_at','open_at']
    success_url = "/restaurants/"
    def get_form(self):
        form = super().get_form()
        form.fields['open_at'].widget = forms.TimeInput(attrs={'type': 'time'})
        form.fields['close_at'].widget = forms.TimeInput(attrs={'type': 'time'})
        return form
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class RestaurantUpdate(LoginRequiredMixin,UpdateView):
    model = Restaurant
    fields = ['name','description','image','city','categories','open_at','close_at']
    success_url = "/restaurants/"
    def get_form(self):
        form = super().get_form()
        form.fields['open_at'].widget = forms.TimeInput(attrs={'type': 'time'})
        form.fields['close_at'].widget = forms.TimeInput(attrs={'type': 'time'})
        return form


class RestaurantDelete(LoginRequiredMixin,DeleteView):
    model = Restaurant
    fields = "__all__"
    success_url = "/restaurants/"

@login_required
def restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, "restaurants/details.html", {"restaurant": restaurant})

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


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["phone", "role", "profileImage"]



class ItemList(LoginRequiredMixin, ListView):
    model = Item


class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item


class ItemCreat(LoginRequiredMixin, CreateView):
    model = Item
    fields = "__all__"


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ["name", "description", "image", "price"]


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = "/item"


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




# Cart


def viewCart(request, user_id):
    cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    cart_details = CartDetails.objects.filter(cart=cart).select_related("item")
    for item in cart_details:
        item.name = item.item.name
        item.image = item.item.image
        item.total_price = item.item.price * item.quantity

    return render(
        request, "cart/CartView.html", {"cart": cart, "cart_details": cart_details}
    )


def deleteItemFromCart(request, user_id, item_id):
    cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    itemDeleted = CartDetails.objects.filter(cart=cart, item_id=item_id)
    itemDeleted.delete()
    return redirect(f"/cart/viewCart/{user_id}/")


def increaseQty(request, user_id, item_id):
    cart = cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    updateItem = CartDetails.objects.filter(cart=cart, item_id=item_id).first()
    updateItem.quantity += 1
    updateItem.save()
    return redirect(f"/cart/viewCart/{user_id}/")


def decreaseQty(request, user_id, item_id):
    cart = cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    updateItem = CartDetails.objects.filter(cart=cart, item_id=item_id).first()
    updateItem.quantity -= 1
    updateItem.save()
    return redirect(f"/cart/viewCart/{user_id}/")


def addToCart(request, user_id):
    pass


def changeCartStatus(request, user_id, cart_id):
    # add the cart to the order before changing the status
    old_cart = Cart.objects.filter(customer_id=user_id).first()
    old_cart.cart_status = "ordered"
    old_cart.save()

    new_cart = Cart.objects.create(customerid=user_id, cart_status="active")
    return ()
