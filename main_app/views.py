from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, User, Profile, Cart, CartDetails, Item,Order
from .forms import (
    CustomUserCreationForm,
    UpdateProfileForm,
    UpdateUserForm,
    CustomProfileCreationForm,
    AddToCartForm,
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
    now = datetime.datetime.now().time()
    if request.user.profile.role == "owner":
        restaurants = Restaurant.objects.filter(user=request.user)
    else:
        restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        if restaurant.close_at < restaurant.open_at:
            restaurant.is_open = now >= restaurant.open_at or now <= restaurant.close_at
        else:
            restaurant.is_open = restaurant.open_at <= now < restaurant.close_at
    return render(
        request, "restaurants/index.html", {"restaurants": restaurants, "now": now}
    )


class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = [
        "name",
        "description",
        "image",
        "city",
        "categories",
        "close_at",
        "open_at",
    ]
    success_url = "/restaurants/"

    def get_form(self):
        form = super().get_form()
        form.fields["open_at"].widget = forms.TimeInput(attrs={"type": "time"})
        form.fields["close_at"].widget = forms.TimeInput(attrs={"type": "time"})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RestaurantUpdate(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = [
        "name",
        "description",
        "image",
        "city",
        "categories",
        "open_at",
        "close_at",
    ]
    success_url = "/restaurants/"

    def get_form(self):
        form = super().get_form()
        form.fields["open_at"].widget = forms.TimeInput(attrs={"type": "time"})
        form.fields["close_at"].widget = forms.TimeInput(attrs={"type": "time"})
        return form

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


class RestaurantDelete(LoginRequiredMixin, DeleteView):
    model = Restaurant
    fields = "__all__"
    success_url = "/restaurants/"

    def get_queryset(self):
        return Restaurant.objects.filter(user=self.request.user)


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


def addToCart(request, user_id, item_id, restaurant_id):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(
                customer_id=user_id, cart_status="active"
            ).first()
            itemInCart = CartDetails.objects.filter(cart=cart, item_id=item_id).first()
            if (
                itemInCart
                and itemInCart.comment == (form.cleaned_data.get("comment")).strip()
            ):
                itemInCart.quantity += form.cleaned_data.get("quantity")
                itemInCart.save()
            else:
                newRecord = form.save(commit=False)
                newRecord.cart = cart
                newRecord.item_id = item_id
                newRecord.save()
            return redirect("viewCart", user_id=user_id)
        return redirect("item_detail", pk=item_id)
    return redirect("item_detail", pk=item_id)


class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["add_to_cart_form"] = AddToCartForm()
        return context


class ItemCreate(LoginRequiredMixin, CreateView):
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
    restaurants = []
    for row in cart_details:
        itemInItem = Item.objects.filter(id=row.item_id).first()
        restaurant = Restaurant.objects.filter(id=itemInItem.restaurant_id).first()
        if restaurant.name not in restaurants:
            restaurants.append(restaurant.name)
        row.name = row.item.name
        row.image = row.item.image
        row.total_price = row.item.price * row.quantity
        row.restaurant = restaurant.name

    return render(
        request,
        "cart/CartView.html",
        {"cart": cart, "cart_details": cart_details, "restaurants": restaurants},
    )


def deleteItemFromCart(request, user_id, cartDetail_id):
    cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    itemDeleted = get_object_or_404(
        CartDetails.objects.filter(cart=cart, id=cartDetail_id)
    )
    itemDeleted.delete()
    return redirect(f"/cart/viewCart/{user_id}/")


def increaseQty(request, user_id, cartDetail_id):
    cart = cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    updateItem = CartDetails.objects.filter(cart=cart, id=cartDetail_id).first()
    updateItem.quantity += 1
    updateItem.save()
    return redirect(f"/cart/viewCart/{user_id}/")


def decreaseQty(request, user_id, cartDetail_id):
    cart = cart = Cart.objects.filter(customer_id=user_id, cart_status="active").first()
    updateItem = CartDetails.objects.filter(cart=cart, id=cartDetail_id).first()
    updateItem.quantity -= 1
    updateItem.save()
    return redirect(f"/cart/viewCart/{user_id}/")


def changeCartStatus(request, user_id, cart_id):
    # add the cart to the order before changing the status
    old_cart = Cart.objects.filter(customer_id=user_id).first()
    old_cart.cart_status = "ordered"
    old_cart.save()

    new_cart = Cart.objects.create(customer_id=user_id, cart_status="active")
    return ()

def createOrder(request,user_id):

    cart= Cart.objects.get(
        customer_id=user_id,
        cart_status="active")

    order = Order.objects.create(
        restaurant=cart.restaurant,
        customer_id=user_id,
        total_amount=cart.total_amount,
        order_status='P',

    )

    cart.cart_status = "ordered"
    cart.save()
    return redirect(f"/cart/viewCart/{user_id}/")

def customerOrders(request, user_id):
    orders = Order.objects.filter(customer_id=user_id).order_by("-id")
    return render(request, "orders/customer_orders.html", {"orders" : orders })

def restaurantOrders(request):
    restaurants = Restaurant.objects.filter(user=request.user)
    orders = Order.objects.filter(restaurant__in=restaurants).order_by("-id")
    return render(request, "orders/restaurant_orders.html", {"orders" : orders } )

def mark_order_ready(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user != order.restaurant.user:
        return redirect("home")
    order.order_status = "R"
    order.save()
    return redirect("restaurant_orders", user_id=request.user.id)















