from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20)
    phone_verification_status = models.BooleanField(default=False)
    email_verification_status = models.BooleanField(default=False)
