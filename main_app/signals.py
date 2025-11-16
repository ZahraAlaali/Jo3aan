# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver

# from .models import Cart, Profile


# @receiver(post_save, sender=Profile)
# def create_Cart(sender, instance, created, **kwargs):
#     if created and instance.role == "customer":
#         Cart.objects.create(customer=instance.user, cart_status="active")
