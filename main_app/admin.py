from django.contrib import admin
from .models import Restaurant, Profile, Item, Cart, CartDetails, Order
# Register your models here.


# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(CartDetails)
admin.site.register(Cart)
admin.site.register(Order)
