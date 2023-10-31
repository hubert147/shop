from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import forms
from django import forms
from django.shortcuts import render

from shop.models import Category


# Create your views here.


class AddProduct(forms.Form):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}))


    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))



