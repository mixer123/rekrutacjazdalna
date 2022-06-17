from django import forms
from .models import *
from django.core.validators import FileExtensionValidator
class UserForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['first_name','second_name','last_name','email','pesel']



class KandydatForm(forms.ModelForm):
    class Meta:
        model = Kandydat
        fields = ['clas']



class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Dołącz plik csv',
        help_text='max. 1MB',
        validators=[FileExtensionValidator(allowed_extensions=['csv'])])
