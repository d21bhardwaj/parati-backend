
from celery import shared_task
import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token


@shared_task
def add(a, b):
    return (a+b)

@shared_task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        
        
        subject = 'Thank you for registering to our site'
        message = render_to_string('send/index.html', {
        'user': user,
        
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
         })
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['riteshkew1001@gmail.com']

        send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )




       
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    