from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['first_name','second_name','last_name','email','pesel']



class KandydatForm(forms.ModelForm):
    class Meta:
        model = Kandydat
        fields = ['clas']