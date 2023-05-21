from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_verification_status = models.BooleanField(default=False)
    email_verification_status = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class CancellationPolicy(models.Model):
    free_cancellation_before = models.DateTimeField(blank=True, null=True)
    free_cancellation_possible = models.BooleanField(default=False)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Room(models.Model):
    name = models.CharField(max_length=255)
    photos = models.CharField(max_length=1000)
    description = models.TextField()
    limit = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    children_limit = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    meal = models.CharField(max_length=255)
    hotel = models.ForeignKey(
        'Hotel', on_delete=models.CASCADE, related_name='rooms', null=True)
    cancellation_policy = models.ForeignKey(
        CancellationPolicy,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    is_favorite = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photos = models.CharField(max_length=1000)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    count_reviews = models.PositiveIntegerField()
    stars = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_in_time = models.CharField(max_length=10)
    check_out_time = models.CharField(max_length=10)
    cityName = models.CharField(max_length=255)
    cityId = models.PositiveIntegerField()
    cityTimezone = models.CharField(max_length=255)
    distance = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    cityId = models.PositiveIntegerField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=(
        ('city', 'City'), ('place', 'Place')))

    def __str__(self):
        return self.name
