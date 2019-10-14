# python imports
import requests
import pdb

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

from userapi.models import User, PrefStyleImages, Product
from userapi.serializers import (UserCreateSerializer,
                              UserProfileSerializer,
                              UserListSerializer,
                              ProfileSerializer,
                              StyleImageListSerializer,
                              ProductListSerializer
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

    @staticmethod
    def post(request):
        try:
            serializer = UserListSerializer(data=request.data)

                # from custom_logger import DatabaseCustomLogger
                # d = DatabaseCustomLogger()
                # d.database_logger(123)
            user = User.objects.get(email=request.data.get('email'))
            user_serializer = UserListSerializer(user)
            # send_verification_email.delay(user.pk)
            return Response({
                'status': True,
                'userdetail': user_serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        """
        Logout API for user
        """
        try:
            user = request.data.get('user', None)
            logout(request)
            return Response({'status': True,
                             'message': "logout successfully"},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'status': False},
                            status=status.HTTP_400_BAD_REQUEST)


# class SettingAPIView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def put(self, request, *args, **kwargs):
#         try:
#             return Response({'status': True,
#                              'message': "successfully Update"},
#                             status=status.HTTP_200_OK)
#         except (AttributeError, ObjectDoesNotExist):
#             return Response({'status': False},
#                             status=status.HTTP_400_BAD_REQUEST)


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

    def get_queryset(self):
        return Product.objects.all()







class ProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    __doc__ = "Profile API for user"

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            user_serializer = ProfileSerializer(
                instance=user, data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                data = generate_jwt_token(user, {})
                user_serializer = UserListSerializer(user)
                return Response({
                    'status': True,
                    'token': data['token'],
                    'data': user_serializer.data,
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

    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()
            return Response({'status': True,
                             'message': "User delete"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False,
                             'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)



class UserProfileAPIView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    __doc__ = "User Profile API for user"

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        data = request.data
        signup_data = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),

        }
        user_serializer = UserCreateSerializer(
            instance=request.user, data=signup_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            message = ''
            for error in user_serializer.errors.values():
                message += " "
                message += error[0]
            return Response({'status': False,
                             'message': message},
                            status=status.HTTP_400_BAD_REQUEST)
        profile_data = {
            'designation': data.get('designation'),
            'mobile': data.get('mobile'),
            'fb_id': data.get('fb_id'),
            'g_id': data.get('g_id')
        }

        user_serializer = ProfileSerializer(
            instance=user, data=profile_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            user.delete()
            message = ''
            for error in user_serializer.errors.values():
                message += " "
                message += error[0]
            return Response({'status': False,
                             'message': message},
                            status=status.HTTP_400_BAD_REQUEST)
        

        data = generate_jwt_token(user, {})
        user_serializer = UserProfileSerializer(user)
    

        return Response({
            'status': True,
            'data': user_serializer.data,
        }, status=status.HTTP_200_OK)


class EmailAPIView(APIView):

    __doc__ = "EmailAPIView API for user"

    def get(self, request, format=None):
        email = request.query_params.get('email')
        user = User.objects.filter(email=email)
        if user:
            return Response({'status': False,
                             'message': "Email Already Present"}, status=status.HTTP_200_OK)

        return Response({'status': True,
                         'message': ""}, status=status.HTTP_200_OK)


class SignupAPIView(APIView):

    __doc__ = "SignupAPIView API for user"

    def post(self, request, format=None):
       
        data = request.data
        signup_data = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "password": data.get("password"),
        }
        user_serializer = UserCreateSerializer(data=signup_data)
        if user_serializer.is_valid():
            user_serializer.is_active = False
            user = user_serializer.save()
        else:
            return Response({'status': False,
                             'data': user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        profile_data = {
            'designation': data.get('designation'),
            'mobile': data.get('mobile'),
            'fb_id': data.get('fb_id'),
            'g_id': data.get('g_id')
        }

        user_serializer = ProfileSerializer(
            instance=user, data=profile_data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            user.delete()
            return Response({'status': False,
                             'data': user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


        # data = generate_jwt_token(user, {})
        # user_serializer = UserProfileSerializer(user)
        subject = 'Thank you for registering to our site'
        message = render_to_string('send/index.html', {
            'user': user,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
         })
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )
        return Response({
            'status': True,
            # 'token': data['token'],
            # 'data': user_serializer.data,
            'data': "Email Verification is pending",
        }, status=status.HTTP_200_OK)


class ActivateApi(GenericAPIView):
    
    serializer_class = UserCreateSerializer
    
    __doc__ = "Activation API for user"

    def get( self, request, uidb64, token):
       
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()



# class UserReferralViewSet(GenericAPIView):

#     serializer_class = UserReferralSerializer
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, *args, **kwargs ):

#         uid = urlsafe_base64_encode(force_bytes(request.user.pk))
#         token = account_activation_token.make_token(request.user)
#         referral_url = 'http://18.223.218.199:3000/register?code=%s-%s'%(uid, token)
#         return Response({'status':True, 'referral_url':referral_url}, status=status.HTTP_200_OK)



#     def post(self, request, *args, **kwargs ):

#         try:
#             data = request.data
#             data['user'] = request.user.pk
#             referral_serializer = UserReferralSerializer(data=request.data)
#             if referral_serializer.is_valid():
#                 referral = referral_serializer.save()
#                 #send_activation_email.delay(referral.pk)
#                 uid = urlsafe_base64_encode(force_bytes(request.user.pk))
#                 token = account_activation_token.make_token(request.user)
#                 referral_url = 'http://18.223.218.199:3000/register?code=%s-%s'%(uid, token)

#                 current_site = get_current_site(request)
#                 subject = 'Thank you for registering to our site'
#                 message = render_to_string('send/index2.html', {
#                 'referral_url': referral_url,
#                  })
#                 from_email = settings.EMAIL_HOST_USER
#                 #recipient_list = ['manjughorse91@gmail.com']
#                 recipient_list = [referral.email]
          
#                 send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )

#                 return Response(referral_serializer.data, status=status.HTTP_200_OK)
#             else:
#                 message = ''
#                 for error in referral_serializer.errors.values():
#                     message += " "
#                     message += error[0]
#                 return Response({'status': False,
#                                  'message': message},
#                                 status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'status': False,
#                              'message': str(e)},
#                             status=status.HTTP_400_BAD_REQUEST)


class StyleImageApi(GenericAPIView):
    
    __doc__ = "Get Preferences Style Images"

    serializer_class = StyleImageListSerializer

    def get(self, request, format=None):
        """
        List all pref styles.
        """
        try:
            image = PrefStyleImages.objects.all()
            image_serializer = StyleImageListSerializer(image, many=True)

            images = image_serializer.data
            return Response({'status': True,
                             'Response': images},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)



class ConfirmApi(GenericAPIView):
    
    # serializer_class = UserReferralSerializer
    
    __doc__ = "confirmation API for user"

    def get( self, request, uidb64, token):
       
        try:
            # import pdb; pdb.set_trace()
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.credits = user.credits + 500
            user.save()
        else:
            return HttpResponse('Activation link is invalid!')


class ForgetAPIView(APIView):

    __doc__ = "ForgetAPIView API for user"

    def get(self, request, format=None):
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response({'status': False,
                                 'message': "Email Not Present"}, status=status.HTTP_200_OK)
        
        subject = 'Thank you for registering to our site'
        message = render_to_string('registration/password_reset_email1.html', {
        'user': user,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
         })
        from_email = settings.EMAIL_HOST_USER
         
        recipient_list = [user.email]
      
        send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )


        

        return Response({'status': True,
                     'message': ""}, status=status.HTTP_200_OK)


class ForgetResetAPIView(APIView):

    __doc__ = "ForgetResetAPIView API for user"

    def post(self, request, format=None):

        code = request.data.get('code')
        password = request.data.get('password')
        
        try:
            
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None


class ResendAPIView(APIView):

    __doc__ = "ResendAPIView API for user"

    def get(self, request, format=None):
        email = request.query_params.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return Response({'status': False,
                                 'message': "Email not Present"}, status=status.HTTP_200_OK)

        subject = "Thank you for registering to our site"
        message = render_to_string('send/index.html', {
            'user': user,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
         })
        from_email = settings.EMAIL_HOST_USER
         
        recipient_list = [user.email]
      
        send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )





        return Response({'status': True,
                        'message': ""}, status=status.HTTP_200_OK)


