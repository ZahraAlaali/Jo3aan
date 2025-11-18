from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
import json
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, User, Profile, Cart, CartDetails, Item, Order
from .forms import (
    CustomUserCreationForm,
    UpdateProfileForm,
    UpdateUserForm,
    CustomProfileCreationForm,
    AddToCartForm,
    ItemForm,
)
import datetime
from django import forms

# reset password
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "main_app/password_reset.html"
    email_template_name = "main_app/password_reset_email.html"
    subject_template_name = "main_app/password_reset_subject.txt"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("password_reset")


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
    item_form = ItemForm()
    add_to_cart_form = AddToCartForm()
    return render(
        request,
        "restaurants/details.html",
        {
            "restaurant": restaurant,
            "item_form": item_form,
            "add_to_cart_form": add_to_cart_form,
        },
    )


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


def addToCart(request, user_id, item_id, restaurant_id):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(
                customer_id=user_id, cart_status="active"
            ).first()
            if cart and cart.restaurant_id == restaurant_id:
                itemInCart = CartDetails.objects.filter(
                    cart=cart,
                    item_id=item_id,
                    comment=(form.cleaned_data.get("comment")).strip(),
                ).first()
                if itemInCart:
                    itemInCart.quantity += form.cleaned_data.get("quantity")
                    itemInCart.save()
                else:
                    newRecord = form.save(commit=False)
                    newRecord.cart = cart
                    newRecord.item_id = item_id
                    newRecord.save()
                return redirect(f"/restaurants/{restaurant_id}")
            elif cart and cart.restaurant_id != restaurant_id:
                cart = cart = Cart.objects.get(
                    customer_id=user_id, cart_status="active"
                )
                restaurantInCart = Restaurant.objects.get(id=cart.restaurant_id)
                restaurantRequested = Restaurant.objects.get(id=restaurant_id)
                quantity = form.cleaned_data.get("quantity")
                comment = form.cleaned_data.get("comment")
                return render(
                    request,
                    "cart/confirm_new_cart.html",
                    {
                        "user_id": user_id,
                        "item_id": item_id,
                        "restaurantInCart": restaurantInCart,
                        "restaurantRequested": restaurantRequested,
                        "quantity": quantity,
                        "comment": comment,
                    },
                )

            else:
                cart = Cart(
                    customer_id=user_id,
                    cart_status="active",
                    restaurant_id=restaurant_id,
                )
                cart.save()

                newRecord = CartDetails(
                    cart=cart,
                    item_id=item_id,
                    quantity=form.cleaned_data.get("quantity"),
                    comment=form.cleaned_data.get("comment"),
                )
                newRecord.save()
                return redirect(f"/restaurants/{restaurant_id}/")
        return redirect(f"/restaurants/{restaurant_id}/")
    return redirect(f"/restaurants/{restaurant_id}/")


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


def createNewCart(request, user_id, item_id, restaurant_id):
    if request.method == "POST":
        buttonValue = request.POST.get("decision")
        if buttonValue == "new":
            cart = Cart.objects.get(customer_id=user_id, cart_status="active")
            cart.delete()
            cart = Cart(
                customer_id=user_id,
                cart_status="active",
                restaurant_id=restaurant_id,
            )
            cart.save()

            newRecord = CartDetails(
                cart=cart,
                item_id=item_id,
                quantity=request.POST.get("quantity"),
                comment=request.POST.get("comment"),
            )
            newRecord.save()
            return redirect(f"/restaurants/{restaurant_id}/")
        else:
            return redirect(f"/restaurants/{restaurant_id}/")


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
    for row in cart_details:

        restaurantInData = Restaurant.objects.get(id=cart.restaurant_id)
        restaurant = restaurantInData.name
        row.name = row.item.name
        row.itemImage = row.item.itemImage
        row.total_price = row.item.price * row.quantity
    if cart_details:
        return render(
            request,
            "cart/CartView.html",
            {"cart": cart, "cart_details": cart_details, "restaurant": restaurant},
        )
    else:
        return render(
            request,
            "cart/CartView.html",
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


def createOrder(request, user_id):

    cart = Cart.objects.get(customer_id=user_id, cart_status="active")

    order = Order.objects.create(
        restaurant=cart.restaurant,
        customer_id=user_id,
        total_amount=cart.total_amount,
        order_status="P",
    )

    cart.cart_status = "ordered"
    cart.save()
    return redirect(f"/orders/customer/{user_id}/")


def customerOrders(request, user_id):
    orders = Order.objects.filter(customer_id=user_id).order_by("-id")
    return render(request, "orders/customer_orders.html", {"orders": orders})


def restaurantOrders(request):
    restaurants = Restaurant.objects.filter(user=request.user)
    orders = Order.objects.filter(restaurant__in=restaurants).order_by("-id")
    return render(request, "orders/restaurant_orders.html", {"orders": orders})


def mark_order_ready(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.user != order.restaurant.user:
        return redirect("home")
    order.order_status = "R"
    order.save()
    return redirect("restaurant_orders")


# Items
class ItemDetail(LoginRequiredMixin, DetailView):
    model = Item


class ItemCreat(LoginRequiredMixin, CreateView):
    model = Item
    fields = ["name", "description", "itemImage", "price"]


def add_item(request, restaurant_id):
    form = ItemForm(request.POST, request.FILES)
    if form.is_valid():
        print("here")
        new_Item = form.save(commit=False)
        new_Item.restaurant_id = restaurant_id
        new_Item.save()
    return redirect("restaurant_details", restaurant_id)


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    item_form = ItemForm()
    fields = ["name", "description", "itemImage", "price"]
    success_url = "/restaurants/{restaurant_id}/"


class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = "/restaurants/{restaurant_id}/"


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class cartLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        cart = Cart.objects.get(customer_id=self.request.user.id, cart_status="active")
        context = super(cartLandingPageView, self).get_context_data(**kwargs)
        context.update({"cart": cart, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})
        return context


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart_id = self.kwargs["pk"]
        cart = Cart.objects.get(id=cart_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": cart.total_amount,
                        "product_data": {
                            "name": f"Cart #{cart.id}",
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    "quantity": 1,
                },
            ],
            metadata={"cart_id": cart.id},
            mode="payment",
            success_url=YOUR_DOMAIN + f"/orders/create/{self.request.user.id}/",
            cancel_url="/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json["email"])
            cart_id = self.kwargs["pk"]
            cart = Cart.objects.get(id=cart_id)
            intent = stripe.PaymentIntent.create(
                amount=int(cart.total_amount * 100),
                currency="usd",
                customer=customer["id"],
                metadata={"cart_id": cart.id},
            )
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
