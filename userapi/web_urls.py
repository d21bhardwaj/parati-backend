from django.urls import path
from userapi import web_view
    
urlpatterns = [
    path('form/',web_view.style_form, name='style-form'),
]