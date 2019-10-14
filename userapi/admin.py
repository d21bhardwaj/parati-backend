from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress, UserProfile, UserPreferences, PrefStyleImages, Platforms, Category, Brands, Product, Product_Attribute, Product_Color, Product_Size

# Register your models here.


admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserProfile)
admin.site.register(UserPreferences)
admin.site.register(PrefStyleImages)
admin.site.register(Platforms)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brands)
admin.site.register(Product_Attribute)
admin.site.register(Product_Color)
admin.site.register(Product_Size)
