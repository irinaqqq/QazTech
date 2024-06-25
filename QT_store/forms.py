from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import inlineformset_factory

class FeedbackForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=100, error_messages={'required': 'Это поле обязательно для заполнения'})
    email = forms.EmailField(label='Email', error_messages={'required': 'Это поле обязательно для заполнения'})
    phone = forms.CharField(label='Телефон', max_length=15, error_messages={'required': 'Это поле обязательно для заполнения'})
    message = forms.CharField(label='Сообщение', widget=forms.Textarea, error_messages={'required': 'Это поле обязательно для заполнения'})
    class Meta:
        model = Feedback
        fields = ['name', 'phone', 'email', 'message']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = ProductDescription
        fields = ['title', 'image', 'text']

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1, can_delete=True)
ProductDescriptionFormSet = inlineformset_factory(Product, ProductDescription, form=ProductDescriptionForm, extra=1, can_delete=True)

class RegistrationRequestForm(forms.ModelForm):
    class Meta:
        model = RegistrationRequest
        fields = ['first_name', 'last_name', 'email', 'phone_number']