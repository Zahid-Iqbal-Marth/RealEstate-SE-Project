from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from .models import Customer
from django.forms import TextInput,EmailInput,PasswordInput


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True,widget=TextInput,)
    first_name = forms.CharField(required=True,widget=TextInput)
    last_name = forms.CharField(required=True,widget=TextInput)
    email = forms.EmailField(required=True, widget=EmailInput)
    password=forms.CharField(required=True, widget=PasswordInput)
    TYPE = [
        ('SL','Seller'),
        ('BY', 'Buyer'),
    ]
    Type = forms.ChoiceField(required=True,
    choices=TYPE,
    )



class UpdateUserProfile(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email')

class UpdateProfileDetails(forms.ModelForm):
   class Meta:
        model = Customer
        fields = ('country','city','zip_code','phone','image')


# class UpdateProfileDetails(forms.Form):
#     image = forms.ImageField()
#     country = forms.CharField(required=True,widget=TextInput)
#     city = forms.CharField(required=True,widget=TextInput)
#     zip_code = forms.EmailField(required=True, widget=TextInput)
#     phone=forms.CharField(required=True, widget=TextInput)