from django.contrib import admin
from .models import Restaurant, Profile, Item, Cart

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Cart)
