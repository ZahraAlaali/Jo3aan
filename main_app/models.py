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
    ("maqabah", "Maqabah"),
)
ORDER_STATUS = (
    ("P", "Pending"),
    ("R","Ready"),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    image = models.ImageField(
        upload_to="main_app/static/uploads", null=True, blank=True
    )
    city = models.CharField(max_length=20, choices=CITIES, default=CITIES[0][0])
    categories = models.ManyToManyField(Category)
    open_at = models.TimeField()
    close_at = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
        restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
        customer = models.ForeignKey(User, on_delete=models.CASCADE)
        total_amount=models.FloatField(default=0.0)
        order_status=models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])

        def __str__(self):
            return f"{self.id} {self.get_order_status_display()}"

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(
        upload_to="main_app/static/uploads", null=True, blank=True
    )
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.id})


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField(default=0.0)
    cart_status = models.CharField(max_length=50, choices=STATUS, default=STATUS[0][0])
    items = models.ManyToManyField(Item, through="CartDetails", related_name="carts")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total = 0.0
        for item in self.cartdetails_set.select_related("item").all():
            total += item.item.price * item.quantity
        self.total_amount = total
        Cart.objects.filter(pk=self.pk).update(total_amount=total)


class CartDetails(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    comment = models.TextField(max_length=100, default="", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.save()

    def delete(self, *args, **kwargs):
        cart = self.cart
        super().delete(*args, **kwargs)
        cart.total_amount = 0.0
        cart.save()
