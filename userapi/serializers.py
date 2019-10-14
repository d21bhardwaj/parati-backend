from rest_framework import serializers
from .models import User, UserProfile, UserPreferences, UserAddress, PrefStyleImages, Platforms, Category, Brands, Product, Product_Attribute, Product_Color, Product_Size


class UserAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAddress
        fields = ('address_line1', 'address_line2', 'country', 'city', 'zip')


class UserProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ('title', 'mobile', 'fb_id', 'g_id')



class UserPreferencesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserPreferences
        fields = ('gender', 'dob', 'workstyles', 'weekendstyles', 'brands')


class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

   
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('title', 'mobile', 'fb_id', 'g_id')

    def update(self, instance, validated_data):

        instance.title = validated_data.get('designation', instance.title)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.fb_id = validated_data.get('fb_id', instance.fb_id)
        instance.g_id = validated_data.get('g_id', instance.g_id)
        instance.is_active = True
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


# class UserProfileSerializer(serializers.ModelSerializer):
#     type_data = serializers.SerializerMethodField()  

#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'email', 'role', 'type_data', 'company', 'designation', 'phone_number', 'linkedin_url', 'country', 'profile_image_url', 'credits')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data, *args, **kwargs):
        return super(UserCreateSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

# class CategorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product_Color
#         fields = ('id', 'primary_color', 'secondary_color')

# class BrandSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product_Color
#         fields = ('id', 'primary_color', 'secondary_color')

# class PlatformSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product_Color
#         fields = ('id', 'primary_color', 'secondary_color')



class ProductColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Color
        fields = ('id', 'primary_color', 'secondary_color')


class ProductSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Size
        fields = ('id', 'size', 'availability')


class ProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_Attribute
        fields = ('id', 'attribute_name', 'attribute_value')



class StyleImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrefStyleImages
        fields = ('id', 'style', 'image')


class ProductListSerializer(serializers.ModelSerializer):

    category_id = serializers.CharField(source='category.name')
    brand_id = serializers.CharField(source='brand.brand_name')
    platform_image = serializers.CharField(source='platform.image')
    product_attributes = ProductAttributeSerializer(read_only=True, many=True)
    product_color = ProductColorSerializer(read_only=True, many=True)
    product_size = ProductSizeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('category_id', 'name', 'brand_id', 'image_url', 'platform_image', 'price', 'description', 'product_attributes', 'product_color', 'product_size', 'link')
