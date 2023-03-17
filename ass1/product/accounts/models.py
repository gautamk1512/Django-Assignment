from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

class UserProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='user_profile_images')

class UserLoginOTP(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    active = models.BooleanField(default=True)

class ProductMain(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unique_id = models.UUIDField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ProductImage(models.Model):
    product = models.ForeignKey(ProductMain, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

class UserCartProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductMain, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

class UserCart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(UserCartProduct)
    price = models.DecimalField(max_digits=10, decimal_places=2)
