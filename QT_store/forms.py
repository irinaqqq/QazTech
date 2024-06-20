from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(max_length=254, required=True )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

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
