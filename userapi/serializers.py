from rest_framework import serializers
from .models import *
import pdb


class UserAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserAddress
        fields = ('address_line1', 'address_line2', 'country', 'city', 'zip')


class UserCategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'image_url')


class UserWishlistSerializer(serializers.ModelSerializer):
    
    def validate(self, data, *args, **kwargs):
        return super(UserWishlistSerializer, self).validate(data, *args, **kwargs)


    def create(self, validated_data):

        u_id = validated_data['user']
        p_id = validated_data['product']
        user = User.objects.get(id=u_id['id'])
        product = Product.objects.get(id=p_id['id'])
        userfb = UserWishlist.objects.create(user = user, product = product)
        return userfb

    user_id = serializers.CharField(source='user.id')
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = UserWishlist
        fields = ('user_id', 'product_id')

class UserWardrobeSerializer(serializers.ModelSerializer):
    
    def validate(self, data, *args, **kwargs):
        return super(UserWardrobeSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):

        
        u_id = validated_data['user']
        p_id = validated_data['product']
        user = User.objects.get(id=u_id['id'])
        product = Product.objects.get(id=p_id['id'])
        userfb = UserWardrobe.objects.create(user = user, product = product)
        return userfb

    user_id = serializers.CharField(source='user.id')
    product_id = serializers.CharField(source='product.id')
    
    class Meta:
        model = UserWardrobe
        fields = ('user_id', 'product_id')


class UserFeedbackSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
        return super(UserFeedbackSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):

        
        u_id = validated_data['user']
        p_id = validated_data['product']
        feedback = validated_data['feedback']
        userfb = UserFeedback.objects.update_or_create(user_id = int(u_id['id']), product_id = int(p_id['id']), defaults = {'feedback' : feedback})
        return userfb

    user_id = serializers.CharField(source='user.id')
    product_id = serializers.CharField(source='product.id')
    
    class Meta:
        model = UserFeedback
        fields = ('user_id', 'product_id', 'feedback')


class UserProductScoreSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
        return super(UserProductScoreSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):

        
        u_id = validated_data['user']
        p_id = validated_data['product']
        # feedback = validated_data['feedback']
        score = validated_data['score']
        # pdb.set_trace()
        userfb = UserFeedback.objects.filter(user_id = int(u_id['id']), product_id = int(p_id['id'])).update(score=score)
        # userfb = user_feedback.filter(product_id = int(p_id['id']).update(feedback=feedback, score=score))
        # userfb = UserFeedback.objects.update_or_create(user_id = int(u_id['id']), product_id = int(p_id['id']), defaults ={'score' : score})
        return userfb

    user_id = serializers.CharField(source='user.id')
    product_id = serializers.CharField(source='product.id')
    
    class Meta:
        model = UserFeedback
        fields = ('user_id', 'product_id', 'score')


class UserBrandPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrefBrandImages
        fields = ('brand_id', 'image')

class UserStylePreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrefStyleImages
        fields = ('id', 'image')



class UserPreferencesSerializer(serializers.ModelSerializer):
    
    user_id = serializers.CharField(source='user.id')
    
    def validate(self, data, *args, **kwargs):
        return super(UserPreferencesSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):
        
        u_id = validated_data['user']
        gender = validated_data['gender']
        dob = validated_data['dob']
        workstyles = validated_data['workstyles']
        weekendstyles = validated_data['weekendstyles']
        brands = validated_data['brands']
        userpref = UserPreferences.objects.update_or_create(user_id = int(u_id['id']), defaults= {'gender' : gender, 'dob' : dob, 'workstyles' : workstyles, 'weekendstyles' : weekendstyles, 'brands' : brands})
        # userpref = UserPreferences.objects.create(user = user, gender = gender, dob = dob, workstyles = workstyles, weekendstyles = weekendstyles, brands = brands)
        # userpref.save()
        return userpref

    # def update(self, instance, validated_data):

    #     instance.user = validated_data.get('user', instance.user)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.dob = validated_data.get('dob', instance.dob)
    #     instance.workstyles = validated_data.get('workstyles', instance.workstyles)
    #     instance.weekendstyles = validated_data.get('weekendstyles', instance.weekendstyles)
    #     instance.brands = validated_data.get('brands', instance.brands)
    #     instance.save()
    #     return instance


    class Meta:

        model = UserPreferences
        fields = ('user_id','gender', 'dob', 'workstyles', 'weekendstyles', 'brands')


class UserPreferencesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreferences
        fields = ('gender', 'dob', 'workstyles', 'weekendstyles', 'brands')

class UserProfilePreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserPreferences
        fields = ('gender', 'dob')


class UserSecondaryPreferencesSerializer(serializers.ModelSerializer):
    
    
    def validate(self, data, *args, **kwargs):
        return super(UserSecondaryPreferencesSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):
        u_id = self.context.get("user_id")
        body_type = validated_data['body_type']
        t_size = validated_data['t_size']
        t_fit = validated_data['t_fit']
        b_size = validated_data['b_size']
        b_fit = validated_data['b_fit']
        hair_color = validated_data['hair_color']
        skin_color = validated_data['skin_color']
        userpref = UserSecondaryPreferences.objects.update_or_create(user_id = int(u_id), defaults= {'body_type' : body_type, 't_size' : t_size, 't_fit' : t_fit, 'b_size' : b_size, 'b_fit' : b_fit, 'hair_color' : hair_color, 'skin_color' : skin_color})
        return userpref

    class Meta:

        model = UserSecondaryPreferences
        fields = ('body_type', 't_size', 't_fit', 'b_size', 'b_fit', 'hair_color', 'skin_color')


class UserSecondaryPreferencesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSecondaryPreferences
        fields = ('body_type', 't_size', 't_fit', 'b_size', 'b_fit', 'hair_color', 'skin_color')


class UserScoreSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField(source='user.id')
    
    def validate(self, data, *args, **kwargs):
        return super(UserScoreSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):
        # pdb.set_trace()
        u_id = validated_data['user']
        stype = validated_data['score_type']
        cluster = validated_data['score_cluster']
        value = validated_data['score_value']
        userpref = UserScore.objects.update_or_create(user_id = int(u_id['id']), score_type = stype, score_cluster = cluster,defaults = {'score_value' : value})
        # userpref.save()
        return userpref


    class Meta:

        model = UserScore
        fields = ('user_id', 'score_type', 'score_cluster', 'score_value')


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

class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = ('__all__')


class UserProfileSerializer(serializers.ModelSerializer):
    
    address = UserAddressSerializer(read_only=True)
    # user_address = serializers.CharField(source='address')

    class Meta:
        model = UserProfile
        fields = ('address', 'title', 'mobile')


class UserListSerializer(serializers.ModelSerializer):

    user_preferences = UserProfilePreferencesSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_preferences', 'user_profile')



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


class UserUpdateSerializer(serializers.ModelSerializer):
    

    # def validate(self, data, *args, **kwargs):
    #     return super(UserUpdateSerializer, self).validate(data, *args, **kwargs)

    
    def update(self, validated_data):

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        user = User.objects.update_or_create(email=email, defaults = {'first_name':first_name, 'last_name':last_name})
        # user = User.objects.get(email=email)
        # user.set_first_name(first_name)
        # user.set_last_name(last_name)
        # user.save()
        return user

    user_preferences = UserPreferencesSerializer(read_only=True)
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_preferences', 'user_profile')

# class CategorySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product_Color
#         fields = ('id', 'primary_color', 'secondary_color')

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brands
        fields = ('id', 'brand_name')

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'price')

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('id', 'color')

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Size
        fields = ('id', 'size')

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Attribute
        fields = ('attribute_name', 'attribute_value')

class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designs
        fields = ('id', 'design')


class FilterSerializer(serializers.ModelSerializer):


    category_brands = BrandSerializer(read_only=True, many=True)
    category_product = PriceSerializer(read_only=True,many=True)
    category_color = ColorSerializer(read_only=True, many=True)
    category_attribute = AttributeSerializer(read_only=True, many=True)
    category_size = SizeSerializer(read_only=True, many=True)
    category_design = DesignSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ('id', 'category_brands', 'category_product', 'category_color', 'category_size', 'category_design', 'category_attribute') #



class ProductClusterSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')
    category_id = serializers.CharField(source='category.id')

    def validate(self, data, *args, **kwargs):
        return super(ProductClusterSerializer, self).validate(data, *args, **kwargs)

    
    def create(self, validated_data):
        product_cluster = ProductCluster.objects.create(**validated_data)
        product_cluster.save()
        return product_cluster


    class Meta:
        model = ProductCluster
        fields = ('id', 'product_id','category_id', 'brand_cluster', 'color_cluster', 'design_cluster')



class ProductColorSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = Product_Color
        fields = ('id', 'product_id', 'primary_color', 'secondary_color')


class ProductSizeSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = Product_Size
        fields = ('id', 'product_id', 'size')


class ProductAttributeSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = Product_Attribute
        fields = ('id', 'product_id', 'attribute_name', 'attribute_value')


class ProductImagesSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = Product_Images
        fields = ('id', 'product_id', 'image_url')



class BrandImageListSerializer(serializers.ModelSerializer):

    brand_id = serializers.CharField(source='brand.id')

    class Meta:
        model = PrefBrandImages
        fields = ('brand_id', 'image')


class StyleImageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrefStyleImages
        fields = ('id', 'style', 'image')


class BrandClusterSerializer(serializers.ModelSerializer):

    category_id = serializers.CharField(source='category.id')
    brand_id = serializers.CharField(source='brand.id')

    class Meta:
        model = BrandCluster
        fields = ('id', 'category_id', 'brand_id', 'cluster')


class ProductListSerializer(serializers.ModelSerializer):

    category_id = serializers.CharField(source='category.id')
    brand_name = serializers.CharField(source='brand.brand_name')
    brand_id = serializers.CharField(source='brand.id')
    primary_color = serializers.CharField(source='primary_color.color')
    design = serializers.CharField(source='design.design')
    platform_image = serializers.CharField(source='platform.image')
    product_attributes = ProductAttributeSerializer(read_only=True, many=True)
    product_size = ProductSizeSerializer(read_only=True, many=True)
    product_images = ProductImagesSerializer(read_only=True, many=True)


    class Meta:
        model = Product
        fields = ('id', 'category_id', 'name', 'brand_id', 'brand_name', 'primary_color', 'design','platform_image', 'price', 'description', 'style_tip', 'product_attributes', 'product_size', 'product_images','link')
