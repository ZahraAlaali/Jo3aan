from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# from phonenumber_field.modelfields import PhoneNumberField

ROLE = (("customer", "Customer"), ("owner", "Owner"))

STATUS = (("active", "active"), ("ordered", "ordered"))

CATEGORIES = (
    ("bahraini", "Bahraini"),
    ("indian", "Indian"),
    ("italian", "Italian"),
    ("japanese", "Japanese"),
    ("chinese", "Chinese"),
    ("korean", "Korean"),
    ("mexican", "Mexican"),
    ("lebanese", "Lebanese"),
    ("egyptian", "Egyptian"),
    ("breakfast", "Breakfast"),
    ("desserts", "Desserts"),
    ("drinks", "Drinks"),
    ("pizza", "Pizza"),
    ("burgers", "Burgers"),
    ("pasta", "Pasta"),
    ("bakery", "Bakery"),
    ("healthy", "Healthy"),
    ("seafood", "Seafood"),
)

CITIES = (
    ("diyar", "Diyar Al-Muharraq"),
    ("dilmunia", "Dilmunia Island"),
    ("m.hidd", "Madinat Al-Hidd"),
    ("sayh", "Al-Sayh"),
    ("busaiteen", "Busaiteen"),
    ("muharraq", "Muharraq"),
    ("arad", "Arad"),
    ("hidd", "Al-Hidd"),
    ("galali", "Galali"),
    ("samaheej", "Samaheej"),
    ("dair", "Al-Dair"),
    ("manama", "Manama"),
    ("rifaa", "Riffa"),
    ("isa.t", "Isa Town"),
    ("hamad.t", "Hamad Town"),
    ("aali", "Aali"),
    ("sitra", "Sitra"),
    ("budaiya", "Budaiya"),
    ("jidhafs", "Jidhafs"),
    ("saar", "Saar"),
    ("sanabis", "Sanabis"),
    ("tubli", "Tubli"),
    ("malkiya", "Malkiya"),
    ("diraz", "Diraz"),
    ("hoora", "Al-Hoora"),
    ("adliya", "Adliya"),
    ("juffair", "Al-Juffair"),
    ("zallaq", "Zallaq"),
    ("amwaj", "Amwaj Islands"),
    ("barbar", "Barbar"),
    ("janabiyah", "Al-Janabiyah"),
    ("salmaniya", "Al-Salmaniya"),
    ("seef", "Al-Seef"),
    ("jannusan", "Jannusan"),
    ("bani.jamra", "Bani Jamra"),
    ("karbabad", "Karbabad"),
    ("naim", "Al-Naim"),
    ("gudaibiya", "Gudaibiya"),
)
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=8)
    # phone = PhoneNumberField()
    role = models.CharField(max_length=50, choices=ROLE, default=ROLE[0][0])
    profileImage = models.ImageField(
        upload_to="main_app/static/uploads/profile_images", default="default.jpg"
    )

    def __str__(self):
        return self.user.username


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    restaurant_description = models.TextField(max_length=250)
    restaurant_image = models.ImageField(
        upload_to="main_app/static/uploads", null=True, blank=True
    )
    city = models.CharField(max_length=20, choices=CITIES, default="")
    category = models.CharField(max_length=20, choices=CATEGORIES, default="")
    close_at = models.TimeField()
    open_at = models.TimeField()


class Cart(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    cart_status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0][0])
    # item_id = models.ManyToManyField(Item)
