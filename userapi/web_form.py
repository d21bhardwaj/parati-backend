from django import forms 
from .web_api import *

class StyleForm(forms.Form):
    gen = {('male','male'),('female','female')}
    gender        = forms.ChoiceField(choices=gen)
    birthday      = forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y'),attrs={'class':'myDateClass', 
                                            'placeholder':'Year-Month-Day'}))
    weekend_style = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    weekday_style = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    brand         = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)
        self.fields['weekend_style'].choices = weekend_choices()
        self.fields['weekday_style'].choices = weekday_choices()
        self.fields['brand'].choices         = brand_choices()
        # self.fields['birthday'].input_formats = ('%Y-%m-%d')