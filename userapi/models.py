from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(('first_name'), max_length=30, blank=True)
    last_name = models.CharField(('last_name'), max_length=30, blank=True)

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='address')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, blank=True, null=True)
    mobile = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=False)
    is_social_login = models.BooleanField(default=False)
    fb_id = models.CharField(max_length=50)
    g_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    workstyles = models.CharField(max_length=500)
    weekendstyles = models.CharField(max_length=500)
    brands = models.CharField(max_length=500)


class PrefStyleImages(models.Model):
    image = models.CharField(max_length=50)
    style = models.CharField(max_length=10)
    tdesign_cluster = models.CharField(max_length=5)
    tcolor_cluster = models.CharField(max_length=5)
    bdesign_cluster = models.CharField(max_length=5)
    bcolor_cluster = models.CharField(max_length=5)


class Platforms(models.Model):
    name = models.CharField(max_length=20)
    image = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)


class Brands(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brands')
    brand_name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=50)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    platform = models.ForeignKey(Platforms, on_delete=models.CASCADE, related_name='platform')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, related_name='product_brand')
    image_url = models.CharField(max_length=500)
    link = models.CharField(max_length=500)


class Product_Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    attribute_name = models.CharField(max_length=20)
    attribute_value = models.CharField(max_length=20)


class Product_Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_color')
    primary_color = models.CharField(max_length=20)
    secondary_color = models.CharField(max_length=20)


class Product_Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_size')
    size = models.CharField(max_length=5)
    availability = models.CharField(max_length=5)





