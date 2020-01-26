from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1','password2')