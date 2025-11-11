from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

ROLE = (("customer", "Customer"), ("owner", "Owner"))
# Create your models here.


class Profile(models.Model):
    username = models.CharField(max_length=50)
    phone = PhoneNumberField()
    role = models.CharField(max_length=50, choices=ROLE, default=ROLE[0][0])
    profileImage = models.ImageField(upload_to="main_app/static/uploads", default="")
