# python imports
import requests
import pdb
from collections import Counter
from random import shuffle

# Django imports
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

# Rest Framework imports
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# local imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView

from userapi.models import User, PrefStyleImages, Product, PrefBrandImages, Category, UserPreferences, UserWishlist, UserWardrobe, BrandCluster, UserScore, ProductCluster, UserFeedback, UserSecondaryPreferences, UserProfile, UserAddress, Colors
from userapi.serializers import (UserCreateSerializer,
                              UserProfileSerializer,
                              UserListSerializer,
                              ProfileSerializer,
                              StyleImageListSerializer,
                              ProductListSerializer,
                              BrandImageListSerializer,
                              UserPreferencesSerializer,
                              UserCategoriesSerializer,
                              UserPreferencesListSerializer,
                              UserFeedbackSerializer,
                              UserWishlistSerializer,
                              UserWardrobeSerializer,
                              UserScoreSerializer,
                              BrandClusterSerializer,
                              ProductClusterSerializer,
                              UserProductScoreSerializer,
                              FilterSerializer,
                              UserBrandPreferenceSerializer,
                              UserStylePreferenceSerializer,
                              UserUpdateSerializer,
                              UserSecondaryPreferencesSerializer,
                              UserSecondaryPreferencesListSerializer,
                              UserProfilePreferencesSerializer
                              )
from userapi.utils import generate_jwt_token
from userapi.tasks import add, send_verification_email




class RegistrationAPIView(APIView):
    serializer_class = UserCreateSerializer

    __doc__ = "Registration API for user"

    def post(self, request, *args, **kwargs):
        try:
            # pdb.set_trace()
            user_serializer = UserCreateSerializer(data=request.data)
            # pdb.set_trace()
            if user_serializer.is_valid():
                user = user_serializer.save()
                data = generate_jwt_token(user, {})
                user_serializer = UserListSerializer(user)
                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'token': data['token'],
                    'userdetail': user_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in user_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = UserListSerializer

    __doc__ = "Log In API for user which returns token"

    # @staticmethod
    # def post(request):
    #     try:
    #         serializer = UserListSerializer(data=request.data)

    #             # from custom_logger import DatabaseCustomLogger
    #             # d = DatabaseCustomLogger()
    #             # d.database_logger(123)
    #         user = User.objects.get(email=request.data.get('email'))
    #         user_serializer = UserListSerializer(user)
    #         # send_verification_email.delay(user.pk)
    #         return Response({
    #             'status': True,
    #             'userdetail': user_serializer.data,
    #         }, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'status': False,
    #                          'message': str(e)},
    #                         status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        email = request.query_params.get('email')
        
        
        try:

            
            user = User.objects.get(email=email)
            #data = generate_jwt_token(user, {})
            user_serializer = UserListSerializer(user)
            return Response({
                    'status': True,
                    #'token': data['token'],
                    'userdetail': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'token': '',
                    'userdetail': ''}, status=status.HTTP_200_OK)



class UserAPIView(GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        List all the users.
        """
        try:
            users = User.objects.all()
            user_serializer = UserListSerializer(users, many=True)

            users = user_serializer.data
            return Response({'status': True,
                             'Response': users},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)



class ProductAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get(self, request, format=None):
        try:
            scoreList = []
            maxId = 0
            minId = 0
            category_id = request.query_params.get('category_id')
            startCount = int(request.query_params.get('startCount')) - 1
            endCount = startCount + 50
            user_id = request.query_params.get('user_id')
            category = Category.objects.get(id=category_id)
            feedbackProductIds = UserFeedback.objects.filter(user=user_id, feedback__gt=0).values_list('id',flat=True)

            # pdb.set_trace()
            ProductScore = UserFeedback.objects.filter(user=user_id, feedback=0, category_id=category_id).exclude(id__in=feedbackProductIds).order_by('-score').values_list('product_id',flat=True)
            limitproduct_id = list(ProductScore)[startCount:endCount]
            products_sorted = Product.objects.filter(category_id=category_id, id__in = limitproduct_id).order_by('price')
            user_serializer = ProductListSerializer(products_sorted, many=True)
            return Response({
                    'status': True,
                    #'token': data['token'],
                    'products': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'Item does not exist',
                    'products': ''}, status=status.HTTP_200_OK)

            # if int(category_id) <= 3:
            #     color_type = 'tcolor'
            #     design_type = 'tdesign' 
            # else:
            #     color_type = 'bcolor'
            #     design_type = 'bdesign'
            # user_id = request.query_params.get('user_id')
            # category = Category.objects.get(id=category_id)
            # feedbackProductIds = UserFeedback.objects.filter(user=user_id, feedback__isnull=False).values_list('product_id',flat=True)
            # products = Product.objects.filter(category_id=category_id).exclude(id__in=feedbackProductIds)
            # user_score = UserScore.objects.filter(user=user_id)

            # for product in products:
            #     data={}
            #     data['product'] = product
            #     product_cluster = ProductCluster.objects.get(product=product.id,category=product.category_id)
            #     brand_cluster = product_cluster.brand_cluster
            #     color_cluster = product_cluster.color_cluster
            #     design_cluster = product_cluster.design_cluster
            #     score = user_score.get(score_cluster=brand_cluster, score_type='brand').score_value + user_score.get(score_cluster=color_cluster, score_type=color_type).score_value + user_score.get(score_cluster=design_cluster, score_type=design_type).score_value
            #     data['score'] = score
            #     scoreList.append(data)
            
            # productsort = sorted(scoreList, key = lambda i: i['score'],reverse=True)
            # products_sorted = [d['product'] for d in productsort]
            # user_serializer = ProductListSerializer(products_sorted[startCount:endCount], many=True)


class UserProfileAPIView(APIView):
    

    __doc__ = "User Profile API for user"

    def get(self, request, format=None):
        u_id = request.query_params.get('user_id')
        
        
        try:
            user = User.objects.get(id=u_id)
            #data = generate_jwt_token(user, {})
            user_serializer = UserListSerializer(user)
            return Response({
                    'status': True,
                    #'token': data['token'],
                    'userdetail': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'token': '',
                    'userdetail': ''}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            # pdb.set_trace()
            u_id = request.query_params.get('user_id')
            first_name = request.data["userdetail"]["first_name"]
            last_name = request.data["userdetail"]["last_name"]
            email = request.data["userdetail"]["email"]
            gender = request.data["userdetail"]["user_preferences"]["gender"]
            dob = request.data["userdetail"]["user_preferences"]["dob"]
            address_line1 = request.data["userdetail"]["user_profile"]["address"]["address_line1"]
            address_line2 = request.data["userdetail"]["user_profile"]["address"]["address_line2"]
            country = request.data["userdetail"]["user_profile"]["address"]["country"]
            city = request.data["userdetail"]["user_profile"]["address"]["city"]
            zip_code = request.data["userdetail"]["user_profile"]["address"]["zip"]
            title = request.data["userdetail"]["user_profile"]["title"]
            mobile = request.data["userdetail"]["user_profile"]["mobile"]
            
            user = User.objects.update_or_create(email=email, id = int(u_id), defaults = {'first_name':first_name, 'last_name':last_name})
            user_preferences = UserPreferences.objects.update_or_create(user_id = int(u_id), defaults = {'gender':gender, 'dob':dob})
            user_profile = UserProfile.objects.update_or_create(user_id = int(u_id), defaults = {'title':title, 'mobile':mobile})
            user_address = UserAddress.objects.update_or_create(user_id = int(u_id), defaults = {'address_line1':address_line1, 'address_line2':address_line2, 'country':country, 'city':city, 'zip':zip_code})
            
            # pdb.set_trace()

            return Response({
                    'status': True,
                    # 'token': data['token'],
                    'message' : 'User Profile updated successfully.'
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class UserFeedbackAPIView(GenericAPIView):

    __doc__ = "Insert user product feedback"

    serializer_class = UserFeedbackSerializer

    def post(self, request, format=None):
        try:
            feedback = request.data['values']
            feedback_serializer = UserFeedbackSerializer(data=feedback, many=True)
            if feedback_serializer.is_valid():
                upref = feedback_serializer.save()
                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'message' : "Feedback saved"
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in feedback_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)



class StyleImageApi(GenericAPIView):
    
    __doc__ = "Get Preferences Style Images"

    serializer_class = StyleImageListSerializer

    def get(self, request, format=None):
        """
        List all pref styles.
        """
        try:
            gender = request.query_params.get('gender')
            if gender == 'M':
                image = PrefStyleImages.objects.filter(id__lt=97).order_by('?')
            else:
                image = PrefStyleImages.objects.filter(id__gt=96).order_by('?')
            image_serializer = StyleImageListSerializer(image, many=True)

            images = image_serializer.data
            return Response({'status': True,
                             'Response': images},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class CategoriesApi(GenericAPIView):
    
    __doc__ = "Get Categories"

    serializer_class = UserCategoriesSerializer


    def get(self, request, format=None):
        """
        List all pref styles.
        """
        user_id = request.query_params.get('user_id')

        try:
            user =  UserPreferences.objects.get(user_id=user_id)
            gender = user.gender[0]
            if gender == 'M':
                image = Category.objects.filter(id__lt=11)
            else:
                image = Category.objects.filter(id__gt=10)
            image_serializer = UserCategoriesSerializer(image, many=True)

            images = image_serializer.data
            return Response({'status': True,
                             'Response': images},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class FilterApi(GenericAPIView):
    
    __doc__ = "Filters"

    serializer_class = FilterSerializer


    def get(self, request, format=None):
        """
        
        """
        category_id = request.query_params.get('category_id')

        try:
            temp = {}
            price_range = {}
            filtered_data = []
            category = Category.objects.get(id=category_id)
            category_serializer = FilterSerializer(category)
            filter_data = category_serializer.data
            prices = list(float(d['price']) for d in filter_data['category_product'])
            price_range['max_price'] = max(prices)
            price_range['min_price'] = min(prices)
            # price['Price'] = price_range
            temp['Colors'] = list((d['color']) for d in filter_data['category_color'])
            temp['Sizes'] = list(set((d['size']) for d in filter_data['category_size']))
            temp['Designs'] = list((d['design']) for d in filter_data['category_design'])
            attributes = list(set(d['attribute_name'] for d in filter_data['category_attribute']))
            for attribute in attributes:
                temp[str(attribute)] = set(list((d['attribute_value']) for d in filter_data['category_attribute'] if (d['attribute_name'] == str(attribute) and d['attribute_value'] != 'null' and d['attribute_value'] != '')))
            for key in temp.keys():
                var = {}
                var['heading'] = key
                var['content'] = temp[key]
                filtered_data.append(var)

            return Response({'status': True,
                             'filter_data': filtered_data,
                             'Brands' : filter_data['category_brands'],
                             'Prices' : price_range},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            prices = request.data['prices']
            colors = request.data['colors'].split(',')
            color_ids = Colors.objects.filter(color__in=colors)
            brand_ids = request.data['brands'].split(',')
            category_id = request.query_params.get('category_id')
            startCount = int(request.query_params.get('startCount')) - 1
            endCount = startCount + 50
            user_id = request.query_params.get('user_id')
            category = Category.objects.get(id=category_id)
            feedbackProductIds = UserFeedback.objects.filter(user=user_id, feedback__gt=0).values_list('product_id',flat=True)
            ProductScore = UserFeedback.objects.filter(user=user_id, feedback=0).order_by('-score').values_list('product_id',flat=True)
            limitproduct_id = list(ProductScore)
            products_sorted = Product.objects.filter(category_id=category_id, id__in = limitproduct_id).exclude(id__in=feedbackProductIds)
            if len(brand_ids)>0 and len(brand_ids[0])>0:
                product_filter = products_sorted.filter(brand_id__in=brand_ids)
            else:
                product_filter = products_sorted
            
            if len(colors)>0 and len(colors[0])>0:
                product_filter = product_filter.filter(primary_color_id__in=color_ids)
            else:
                product_filter = product_filter

            if len(prices)>0:
                max_price = int(prices['max_price']) + 1
                min_price = int(prices['min_price']) - 1
                product_filter = product_filter.filter(price__lt=max_price, price__gt=min_price)
            else:
                product_filter = product_filter

            if len(product_filter) < int(endCount):
                endCount = len(product_filter)-1

            if endCount>0:
                user_serializer = ProductListSerializer(product_filter[startCount:endCount], many=True)
                return Response({
                        'status': True,
                        'request': request.data,
                        'products': user_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({
                        'status': True,
                        'request': request.data,
                        'products': 'No Product matching the filters found.'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'Item does not exist',
                    'products': ''}, status=status.HTTP_200_OK)


class BrandImageApi(GenericAPIView):
    
    __doc__ = "Get Preferences Brand Images"

    serializer_class = BrandImageListSerializer

    def get(self, request, format=None):
        """
        List all pref styles.
        """
        try:
            gender = request.query_params.get('gender')
            if gender == 'M':
                image = PrefBrandImages.objects.filter(id__lt=33)
            else:
                image = PrefBrandImages.objects.filter(id__gt=32)
            image_serializer = BrandImageListSerializer(image, many=True)

            images = image_serializer.data
            return Response({'status': True,
                             'Response': images},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)




class UserPreferenceAPIView(APIView):
    serializer_class = UserPreferencesSerializer

    __doc__ = "User Preference API for user "


    def post(self, request, format=None):
        try:
            # pdb.set_trace()
            serializer = UserPreferencesSerializer(data=request.data)
            brandClusterScore = {'1' : 0,'2' : 0,'3' : 0,'4' : 0,'5' : 0, '6' : 0}
            colorClusterScore = {'1' : 0,'2' : 0,'3' : 0,'4' : 0}
            designClusterScore = {'1' : 0,'2' : 0,'3' : 0,'4' : 0,'5' : 0, '6' : 0}
            # pdb.set_trace()
            if serializer.is_valid():
                upref = serializer.save()
                upref_serializer = UserPreferencesListSerializer(upref[0])

                #brand score
                brandId = upref_serializer.data['brands'].split(',')
                prefBrandsId = PrefBrandImages.objects.filter(brand_id__in=brandId)
                prefBrandClusterCounts = dict(Counter(prefBrandsId.values_list('cluster',flat=True)))
                prefBrandTotalCount = prefBrandsId.count()
                maxBrandClusters = Counter(prefBrandsId.values_list('cluster',flat=True)).most_common(1)
                maxBrandClusterCount = maxBrandClusters[0][1]
                # for prefBrandCluster in prefBrandClusterCounts.keys():
                #     brandClusterScore[prefBrandCluster] = prefBrandClusterCounts[prefBrandCluster]/maxBrandClusterCount
                
                notSelectedCluster = { k : brandClusterScore[k] for k in set(brandClusterScore) - set(prefBrandClusterCounts) }
                if len(notSelectedCluster) > 0:
                    minBrandCluster = next(iter(notSelectedCluster.items()))
                    minBrandClusterCount = minBrandCluster[1]
                else : 
                    minBrandCluster = Counter(prefBrandsId.values_list('cluster',flat=True)).most_common()[:-2:-1][0]
                    minBrandClusterCount = minBrandCluster[1]
                BrandClusterScore = []
                for cluster in brandClusterScore:
                    userBrandClusterScore = {}
                    userBrandClusterScore['user_id'] = request.data['user_id']
                    userBrandClusterScore['score_type'] = "brand"
                    userBrandClusterScore['score_cluster'] = int(cluster)
                    userBrandClusterScore['score_value'] = round(0.1 + 0.9*( (prefBrandClusterCounts.get(cluster,0) - minBrandClusterCount)/(maxBrandClusterCount - minBrandClusterCount) ),2)
                    BrandClusterScore.append(userBrandClusterScore)
                # pdb.set_trace()
                userClusterScoreSeralizer = UserScoreSerializer(data=BrandClusterScore, many=True)
                if userClusterScoreSeralizer.is_valid():
                    userClusterScoreSeralizer.save()

                # #style scores
                # styleId = (upref_serializer.data['weekendstyles'].split(',')) + (upref_serializer.data['workstyles'].split(','))
                # prefStyleId = PrefStyleImages.objects.filter(id__in=styleId)
                # prefStyleTotalCount = prefStyleId.count()

                #color score
                #topwear
                styleId = (upref_serializer.data['workstyles'].split(','))
                prefStyleId = PrefStyleImages.objects.filter(id__in=styleId)
                prefStyleTotalCount = prefStyleId.count()

                prefTcolorClusterCounts = dict(Counter(prefStyleId.values_list('tcolor_cluster',flat=True)))
                maxTcolorClusters = Counter(prefStyleId.values_list('tcolor_cluster',flat=True)).most_common(1)
                maxTcolorClusterCount = maxTcolorClusters[0][1]

                notSelectedCluster = { k : colorClusterScore[k] for k in set(colorClusterScore) - set(prefTcolorClusterCounts) }
                if len(notSelectedCluster) > 0:
                    minTcolorCluster = next(iter(notSelectedCluster.items()))
                    minTcolorClusterCount = minTcolorCluster[1]
                else : 
                    minTcolorCluster = Counter(prefStyleId.values_list('tcolor_cluster',flat=True)).most_common()[:-2:-1][0]
                    minTcolorClusterCount = minTcolorCluster[1]
                ColorClusterScore = []
                for cluster in colorClusterScore:
                    userTColorClusterScore = {}
                    userTColorClusterScore['user_id'] = request.data['user_id']
                    userTColorClusterScore['score_type'] = "tcolor"
                    userTColorClusterScore['score_cluster'] = int(cluster)
                    userTColorClusterScore['score_value'] = round(0.1 + 0.9*( (prefTcolorClusterCounts.get(cluster,0) - minTcolorClusterCount)/(maxTcolorClusterCount - minTcolorClusterCount) ),2)
                    ColorClusterScore.append(userTColorClusterScore)
                # pdb.set_trace()
                userClusterScoreSeralizer = UserScoreSerializer(data=ColorClusterScore, many=True)
                if userClusterScoreSeralizer.is_valid():
                    userClusterScoreSeralizer.save()
                
                # for prefTcolorCluster in prefTcolorClusterCounts.keys():
                #     colorClusterScore[prefTcolorCluster] = prefTcolorClusterCounts[prefTcolorCluster]/maxTcolorClusterCount
                # for cluster in colorClusterScore:
                #     userTColorClusterScore['score_cluster'] = int(cluster)
                #     userTColorClusterScore['score_value'] = round(colorClusterScore[cluster],2)
                #     userClusterScoreSeralizer = UserScoreSerializer(data=userTColorClusterScore)
                #     if userClusterScoreSeralizer.is_valid():
                #         userClusterScoreSeralizer.save()

                #bottomwear
                styleId = (upref_serializer.data['weekendstyles'].split(','))
                prefStyleId = PrefStyleImages.objects.filter(id__in=styleId)
                prefStyleTotalCount = prefStyleId.count()

                prefBcolorClusterCounts = dict(Counter(prefStyleId.values_list('bcolor_cluster',flat=True)))
                maxBcolorClusters = Counter(prefStyleId.values_list('bcolor_cluster',flat=True)).most_common(1)
                maxBcolorClusterCount = maxBcolorClusters[0][1]

                notSelectedCluster = { k : colorClusterScore[k] for k in set(colorClusterScore) - set(prefBcolorClusterCounts) }
                if len(notSelectedCluster) > 0:
                    minBcolorCluster = next(iter(notSelectedCluster.items()))
                    minBcolorClusterCount = minBcolorCluster[1]
                else : 
                    minBcolorCluster = Counter(prefStyleId.values_list('bcolor_cluster',flat=True)).most_common()[:-2:-1][0]
                    minBcolorClusterCount = minBcolorCluster[1]
                ColorClusterScore = []
                for cluster in colorClusterScore:
                    userBColorClusterScore = {}
                    userBColorClusterScore['user_id'] = request.data['user_id']
                    userBColorClusterScore['score_type'] = "bcolor"
                    userBColorClusterScore['score_cluster'] = int(cluster)
                    userBColorClusterScore['score_value'] = round(0.1 + 0.9*( (prefBcolorClusterCounts.get(cluster,0) - minBcolorClusterCount)/(maxBcolorClusterCount - minBcolorClusterCount) ),2)
                    ColorClusterScore.append(userBColorClusterScore)
                # pdb.set_trace()
                userClusterScoreSeralizer = UserScoreSerializer(data=ColorClusterScore, many=True)
                if userClusterScoreSeralizer.is_valid():
                    userClusterScoreSeralizer.save()

                # for prefBcolorCluster in prefBcolorClusterCounts.keys():
                #     colorClusterScore[prefBcolorCluster] = prefBcolorClusterCounts[prefBcolorCluster]/maxBcolorClusterCount
                # for cluster in colorClusterScore:
                #     userBColorClusterScore['score_cluster'] = int(cluster)
                #     userBColorClusterScore['score_value'] = round(colorClusterScore[cluster],2)
                #     userClusterScoreSeralizer = UserScoreSerializer(data=userBColorClusterScore)
                #     if userClusterScoreSeralizer.is_valid():
                #         userClusterScoreSeralizer.save()
                # pdb.set_trace()


                #design score
                #topwear
                styleId = (upref_serializer.data['workstyles'].split(','))
                prefStyleId = PrefStyleImages.objects.filter(id__in=styleId)
                prefStyleTotalCount = prefStyleId.count()


                prefTdesignClusterCounts = dict(Counter(prefStyleId.values_list('tdesign_cluster',flat=True)))
                maxTdesignClusters = Counter(prefStyleId.values_list('tdesign_cluster',flat=True)).most_common(1)
                maxTdesignClusterCount = maxTdesignClusters[0][1]
                
                # for prefTdesignCluster in prefTdesignClusterCounts.keys():
                #     designClusterScore[prefTdesignCluster] = prefTdesignClusterCounts[prefTdesignCluster]/maxTdesignClusterCount
                # for cluster in designClusterScore:
                #     userTDesignClusterScore['score_cluster'] = int(cluster)
                #     userTDesignClusterScore['score_value'] = round(designClusterScore[cluster],2)
                #     userClusterScoreSeralizer = UserScoreSerializer(data=userTDesignClusterScore)
                #     if userClusterScoreSeralizer.is_valid():
                #         userClusterScoreSeralizer.save()

                notSelectedCluster = { k : designClusterScore[k] for k in set(designClusterScore) - set(prefTdesignClusterCounts) }
                if len(notSelectedCluster) > 0:
                    minTdesignCluster = next(iter(notSelectedCluster.items()))
                    minTdesignClusterCount = minTdesignCluster[1]
                else : 
                    minTdesignCluster = Counter(prefStyleId.values_list('tdesign_cluster',flat=True)).most_common()[:-2:-1][0]
                    minTdesignClusterCount = minTdesignCluster[1]
                DesignClusterScore = []
                for cluster in designClusterScore:
                    userTDesignClusterScore = {}
                    userTDesignClusterScore['user_id'] = request.data['user_id']
                    userTDesignClusterScore['score_type'] = "tdesign"
                    userTDesignClusterScore['score_cluster'] = int(cluster)
                    userTDesignClusterScore['score_value'] = round(0.1 + 0.9*( (prefTdesignClusterCounts.get(cluster,0) - minTdesignClusterCount)/(maxTdesignClusterCount - minTdesignClusterCount) ),2)
                    DesignClusterScore.append(userTDesignClusterScore)
                # pdb.set_trace()
                userClusterScoreSeralizer = UserScoreSerializer(data=DesignClusterScore, many=True)
                if userClusterScoreSeralizer.is_valid():
                    userClusterScoreSeralizer.save()

                # pdb.set_trace()


                #bottomwear
                styleId = (upref_serializer.data['weekendstyles'].split(','))
                prefStyleId = PrefStyleImages.objects.filter(id__in=styleId)
                prefStyleTotalCount = prefStyleId.count()


                prefBdesignClusterCounts = dict(Counter(prefStyleId.values_list('bdesign_cluster',flat=True)))
                maxBdesignClusters = Counter(prefStyleId.values_list('bdesign_cluster',flat=True)).most_common(1)
                maxBdesignClusterCount = maxBdesignClusters[0][1]

                # for prefBdesignCluster in prefBdesignClusterCounts.keys():
                #     designClusterScore[prefBcolorCluster] = prefBdesignClusterCounts[prefBdesignCluster]/maxBdesignClusterCount
                # for cluster in designClusterScore:
                #     userBDesignClusterScore['score_cluster'] = int(cluster)
                #     userBDesignClusterScore['score_value'] = round(designClusterScore[cluster],2)
                #     userClusterScoreSeralizer = UserScoreSerializer(data=userBDesignClusterScore)
                #     if userClusterScoreSeralizer.is_valid():
                #         userClusterScoreSeralizer.save()

                notSelectedCluster = { k : designClusterScore[k] for k in set(designClusterScore) - set(prefBdesignClusterCounts) }
                if len(notSelectedCluster) > 0:
                    minBdesignCluster = next(iter(notSelectedCluster.items()))
                    minBdesignClusterCount = minBdesignCluster[1]
                else : 
                    minBdesignCluster = Counter(prefStyleId.values_list('bdesign_cluster',flat=True)).most_common()[:-2:-1][0]
                    minBdesignClusterCount = minBdesignCluster[1]
                DesignClusterScore = []
                for cluster in designClusterScore:
                    userBDesignClusterScore = {}
                    userBDesignClusterScore['user_id'] = request.data['user_id']
                    userBDesignClusterScore['score_type'] = "bdesign"
                    userBDesignClusterScore['score_cluster'] = int(cluster)
                    userBDesignClusterScore['score_value'] = round(0.1 + 0.9*( (prefBdesignClusterCounts.get(cluster,0) - minBdesignClusterCount)/(maxBdesignClusterCount - minBdesignClusterCount) ),2)
                    DesignClusterScore.append(userBDesignClusterScore)
                # pdb.set_trace()
                userClusterScoreSeralizer = UserScoreSerializer(data=DesignClusterScore, many=True)
                if userClusterScoreSeralizer.is_valid():
                    userClusterScoreSeralizer.save()

                
                #product score in feedback table
                user_id = request.data['user_id']
                # pdb.set_trace()
                #feedbackProductIds = UserFeedback.objects.filter(user=user_id, feedback__isnull=False).values_list('product_id',flat=True)
                gender = upref_serializer.data['gender']
                if gender[0] == 'M':
                    products = ProductCluster.objects.filter(category_id__lt=11) #.exclude(product_id__in=feedbackProductIds)
                else:
                    products = ProductCluster.objects.filter(category_id__gt=10) #.exclude(product_id__in=feedbackProductIds)
                
                # pdb.set_trace()
                user_score = UserScore.objects.filter(user_id=int(user_id))
                userScore = UserScoreSerializer(user_score, many=True)
                # final_products = ProductClusterSerializer(products, many=True)
                product_scores =[]
                update_product_scores =[]
                for product in products:
                    data={}
                    score=0
                    try:
                        
                        if ((int(product.category_id) <= 3) or ((int(product.category_id) >= 8) 
                            and (int(product.category_id) <= 14)) or ((int(product.category_id) >= 18))):
                            color_type = 'tcolor'
                            design_type = 'tdesign'
                        else:
                            color_type = 'bcolor'
                            design_type = 'bdesign'
                        data['product_id'] = product.product_id
                        data['user_id'] = user_id
                        # data['feedback'] = 0
                        # data['category_id'] = product.category_id
                        # pdb.set_trace()
                        # product_cluster = products.filter(product=product.product_id,category=product.category_id)[0]
                        # product_cluster = (list(filter(lambda iproduct:((int(iproduct['product_id']) == product.product_id) and (int(iproduct['category_id']) == product.category_id)), final_products.data)))
                        # brand_cluster = product_cluster[0]['brand_cluster']
                        # color_cluster = product_cluster[0]['color_cluster']
                        # design_cluster = product_cluster[0]['design_cluster']
                        # pdb.set_trace()
                        brand_cluster = product.brand_cluster
                        color_cluster = product.color_cluster
                        design_cluster = product.design_cluster
                        # pdb.set_trace()
                        score = float(list(filter(lambda score:((score['score_cluster'] == brand_cluster) and (score['score_type'] == 'brand')), userScore.data))[0]['score_value']) + float(list(filter(lambda score:((score['score_cluster'] == color_cluster) and (score['score_type'] == color_type)), userScore.data))[0]['score_value']) + float(list(filter(lambda score:((score['score_cluster'] == design_cluster) and (score['score_type'] == design_type)), userScore.data))[0]['score_value'])
                        #score = user_score.get(score_cluster=brand_cluster, score_type='brand').score_value + user_score.get(score_cluster=color_cluster, score_type=color_type).score_value + user_score.get(score_cluster=design_cluster, score_type=design_type).score_value
                        data['score'] = round(score,2)
                        product_score = UserFeedback(user_id=user_id, product_id=product.product_id,feedback=0,score=score, category_id=product.category_id)
                        # product_updated_score = UserFeedback(user_id=user_id, product_id=product.product_id, score=score, category_id=product.category_id)
                        # product_score = UserProductScoreSerializer(data=data)
                        # if product_score.is_valid():
                        #     product_scores.append(product_score.data)
                        
                        product_scores.append(product_score)

                        update_product_scores.append(data)
                    except Exception as e:
                        data={}
                user_feedbacks = UserFeedback.objects.filter(user_id = user_id)
                # pdb.set_trace()
                product_scores = sorted(product_scores, key = lambda i: i.score)
                if (len(user_feedbacks) > 0):
                    user_feedbacks.delete()
                    # UserFeedback.objects.bulk_create(product_scores)
                    # for user_feedback in user_feedbacks :
                    #     u_id = user_feedback.user_id
                    #     p_id = user_feedback.product_id
                    #     # pdb.set_trace()
                    #     user_feedback.score = float((list(filter(lambda score:((int(score['user_id']) == u_id) and (int(score['product_id']) == p_id)), update_product_scores)))[0]['score'])
                        
                    # product_score = helper.bulk_update(update_product_scores, update_fields=['score'])
                    # product_score = UserProductScoreSerializer(data=update_product_scores, many=True)
                    # pdb.set_trace()
                    # if product_score.is_valid():
                    #     product_score.save()
                # else: UserFeedback.objects.bulk_create(product_scores)

                UserFeedback.objects.bulk_create(product_scores)
                
                    

                # pdb.set_trace()
                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'userdetail': upref_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        id = request.query_params.get('user_id')

        try:
            data = {}
            user = UserPreferences.objects.get(user=id)
            #data = generate_jwt_token(user, {})
            user_serializer = UserPreferencesListSerializer(user)
            brands_ids = user_serializer.data['brands'].split(',')
            workstyles_ids = user_serializer.data['workstyles'].split(',')
            weekendstyles_ids = user_serializer.data['weekendstyles'].split(',')
            data['brands'] = UserBrandPreferenceSerializer(PrefBrandImages.objects.filter(brand_id__in=brands_ids), many=True).data
            data['workstyles'] = UserStylePreferenceSerializer(PrefStyleImages.objects.filter(id__in=workstyles_ids), many=True).data
            data['weekendstyles'] = UserStylePreferenceSerializer(PrefStyleImages.objects.filter(id__in=weekendstyles_ids), many=True).data
            data['gender'] = user_serializer.data['gender']
            data['dob'] = user_serializer.data['dob']

            return Response({
                    'status': True,
                    #'token': data['token'],
                    'userdetail': data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'User Preferences does not exist.'}, status=status.HTTP_200_OK)

class UserSecondaryPreferenceAPIView(APIView):
    serializer_class = UserSecondaryPreferencesSerializer

    __doc__ = "User Secondary Preference API for user "


    def post(self, request, format=None):
        try:
            # pdb.set_trace()
            id = request.query_params.get('user_id')
            serializer = UserSecondaryPreferencesSerializer(data=request.data, context={'user_id': id})
            if serializer.is_valid():
                upref = serializer.save()
                upref_serializer = UserSecondaryPreferencesListSerializer(upref[0])

                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'secondary_preferences': upref_serializer.data,
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        id = request.query_params.get('user_id')

        try:
            data = {}
            user = UserSecondaryPreferences.objects.get(user=id)
            #data = generate_jwt_token(user, {})
            user_serializer = UserSecondaryPreferencesListSerializer(user)

            return Response({
                    'status': True,
                    #'token': data['token'],
                    'userdetail': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'User Secondary Preferences empty.'}, status=status.HTTP_200_OK)


class UserWishlistAPIView(APIView):
    serializer_class = UserWishlistSerializer

    __doc__ = "User WishList"

    def post(self, request, format=None):
        try:
            wishlist_serializer = UserWishlistSerializer(data=request.data)
            if wishlist_serializer.is_valid():
                upref = wishlist_serializer.save()
                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'message' : "Product Added to Wishlist"
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in wishlist_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        id = request.query_params['user_id']

        try:
            wishlist = UserWishlist.objects.filter(user=id).values_list('product_id', flat=True)
            #data = generate_jwt_token(user, {})
            product = Product.objects.filter(id__in = wishlist)
            user_serializer = ProductListSerializer(product, many=True)
            return Response({
                'status': True,
                #'token': data['token'],
                'products': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'User Wishlist empty.'}, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        userid = request.query_params['user_id']
        productid = request.query_params['product_id']

        try:
            wishlist = UserWishlist.objects.filter(user=userid, product=productid)
            wishlist.delete()
            return Response({
                'status': True,
                #'token': data['token'],
                'message': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'Product not found in wishlist.'}, status=status.HTTP_200_OK)

class UserWardrobeAPIView(APIView):
    serializer_class = UserWardrobeSerializer

    __doc__ = "User Wardrobe"

    def post(self, request, format=None):
        try:
            wardrobe_serializer = UserWardrobeSerializer(data=request.data)
            if wardrobe_serializer.is_valid():
                upref = wardrobe_serializer.save()
                # send_verification_email.delay(user.pk)
                return Response({
                    'status': True,
                    'message' : "Product Added to Wardobe"
                }, status=status.HTTP_200_OK)
            else:
                message = ''
                for error in wardrobe_serializer.errors.values():
                    message += " "
                    message += error[0]
                return Response({'status': False,
                                 'message': message},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        id = request.query_params['user_id']

        try:
            wishlist = UserWardrobe.objects.filter(user=id).values_list('product_id', flat=True)
            #data = generate_jwt_token(user, {})
            product = Product.objects.filter(id__in = wishlist)
            user_serializer = ProductListSerializer(product, many=True)
            return Response({
                'status': True if product else False,
                #'token': data['token'],
                'products': user_serializer.data}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'User Wardrobe empty.'}, status=status.HTTP_200_OK)


    def delete(self, request, format=None):
        userid = request.query_params['user_id']
        productid = request.query_params['product_id']

        try:
            wardrobe = UserWardrobe.objects.filter(user=userid, product=productid)
            wardrobe.delete()
            return Response({
                'status': True,
                #'token': data['token'],
                'message': 'Product removed from wardrobe.'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False,
                    'message': 'Product not found in wardrobe.'}, status=status.HTTP_200_OK)

