from django.shortcuts import render, redirect
from .web_form import *
from .web_api import *

def style_form(request):    
    if request.method == "POST":
        form = StyleForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            print(form)
            print('hi') 
        else :
            print(form.errors)   
    else :
        form = StyleForm()
    return render(request, 'web_form/web_form.html', {'form': form})
