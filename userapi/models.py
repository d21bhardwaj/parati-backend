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

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_score')
    score_type = models.CharField(max_length=20)
    score_cluster = models.IntegerField()
    score_value = models.DecimalField(max_digits=3, decimal_places=2)


class UserAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_address')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    title = models.CharField(max_length=5)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, blank=True, null=True, related_name='user_profile_address')
    mobile = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=False)
    is_social_login = models.BooleanField(default=False)
    fb_id = models.CharField(max_length=50)
    g_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_preferences')
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    workstyles = models.CharField(max_length=500)
    weekendstyles = models.CharField(max_length=500)
    brands = models.CharField(max_length=500)


class UserSecondaryPreferences(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_secondary_preferences')
    body_type = models.CharField(max_length=50)
    t_size = models.CharField(max_length=50)
    t_fit = models.CharField(max_length=50)
    b_size = models.CharField(max_length=50)
    b_fit = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    skin_color = models.CharField(max_length=50)




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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_brands')
    brand_name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=50)

class Colors(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_color')
    color = models.CharField(max_length=50)

class Designs(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_design')
    design = models.CharField(max_length=50)

class PrefBrandImages(models.Model):
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, related_name='brands')
    image = models.CharField(max_length=50)
    cluster = models.CharField(max_length=5)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=2000)
    status = models.CharField(max_length=50)
    style_tip = models.CharField(max_length=2000, default=None, blank=True, null=True)
    # platform_product_code = models.CharField(max_length=100, default=None, blank=True, null=True)
    platform = models.ForeignKey(Platforms, on_delete=models.CASCADE, related_name='platform')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, related_name='product_brand')
    primary_color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='product_color_primary')
    design = models.ForeignKey(Designs, on_delete=models.CASCADE, related_name='product_design')
    link = models.CharField(max_length=500)


class ProductCluster(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cluster')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productcluster_category')
    brand_cluster = models.IntegerField()
    color_cluster = models.IntegerField()
    design_cluster = models.IntegerField()

class UserWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlist')
    

class UserWardrobe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wardrobe')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wardrobe')

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_feedback')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_feedback')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_feedback')
    score = models.DecimalField(max_digits=4, decimal_places=3, default=0)
    feedback = models.IntegerField()

class Product_Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_url = models.CharField(max_length=2000)


class Product_Attribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_attributes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_attribute')
    attribute_name = models.CharField(max_length=50)
    attribute_value = models.CharField(max_length=50)


class Product_Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_color')
    primary_color = models.CharField(max_length=20)
    secondary_color = models.CharField(max_length=20)


class Product_Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_size')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_size')
    size = models.CharField(max_length=5)


class BrandCluster(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brandcluster_category')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, related_name='brand')
    cluster = models.IntegerField()


class ColorCluster(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='colorcluster_category')
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, related_name='colors')
    cluster = models.IntegerField()

class DesignCluster(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='designcluster_category')
    design = models.ForeignKey(Designs, on_delete=models.CASCADE, related_name='designs')
    cluster_name = models.CharField(max_length=20, default=None, blank=True, null=True)
    cluster = models.IntegerField()