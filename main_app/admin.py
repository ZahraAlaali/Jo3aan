from django.contrib import admin
from .models import Restaurant, Profile, Item, Cart, CartDetails

# Register your models here.
admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(CartDetails)
admin.site.register(Cart)
