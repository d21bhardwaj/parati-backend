from django.shortcuts import render, redirect
from .web_forms import *
from .web_api import *
import json 
from django.core.serializers.json import DjangoJSONEncoder

def style_form(request):    
    if request.method == "POST":
        form = StyleForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            user_preferences(form) 
        else :
            print(form.errors)   
    else :
        form = StyleForm()
    return render(request, 'web_form/web_form.html', {'form': form})
