from django import forms
from django.forms import ModelForm

from .models import post, media
from django.forms import TextInput
from django.forms import modelformset_factory


class PostCreateForm(forms.Form):

    P_TYPE = [
        ('House','House'),
        ('Plot', 'Plot'),
    ]

    S_TYPE = [
        ('Sale','Sale'),
        ('Rent', 'Rent'),
    ]

    status = forms.ChoiceField(required=True, choices=S_TYPE,)
    location = forms.CharField(required=True, widget=TextInput)
    property_type = forms.ChoiceField(required=True,choices=P_TYPE,)
    area = forms.FloatField(required=True)
    beds = forms.IntegerField(required=False, min_value=0)
    baths = forms.IntegerField(required=False, min_value=0)
    garage = forms.IntegerField(required=False, min_value=0)
    price = forms.FloatField(required=True)
    property_desc = forms.CharField(required=True,widget=forms.Textarea)

    image_field = forms.ImageField(required=False,
         widget=forms.ClearableFileInput(attrs={'multiple': True}))



class UpdatePostForm(forms.ModelForm):
   class Meta:
        model = post
        exclude = ('author',)

class UpdatePostMediaForm(forms.Form):
    image_field = forms.ImageField(required=False,
         widget=forms.ClearableFileInput(attrs={'multiple': True}))



class SearchForm(forms.Form):
    P_TYPE = [
        ('House','House'),
        ('Plot', 'Plot'),
    ]

    S_TYPE = [
        ('Sale','Sale'),
        ('Rent', 'Rent'),
    ]

    status = forms.ChoiceField(required=True, choices=S_TYPE,)
    property_type = forms.ChoiceField(required=True,choices=P_TYPE,)
    city = forms.CharField(required=True)
    beds = forms.IntegerField(required=False, min_value=0)
    baths = forms.IntegerField(required=False, min_value=0)
    garage = forms.IntegerField(required=False, min_value=0)
    price = forms.FloatField(required=True)