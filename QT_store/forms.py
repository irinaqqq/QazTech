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
        fields = ['first_name', 'last_name', 'organization', 'email', 'phone_number']

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = [
            'product', 'note', 'quantity', 'processor', 'mother', 'ram', 
            'storage', 'graphics', 'operating_system', 'screen_sizes', 
            'screen_type', 'screen_resolution', 'touch_screen_touches', 
            'formfactor', 'webcam', 'keyset', 'keyboard_backlight', 
            'power_supplies', 'sizes', 'controllers'
        ]

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super(AddToCartForm, self).__init__(*args, **kwargs)
        if product:
            self.fields['product'].initial = product
            self.fields['processor'].queryset = product.processor.all()
            self.fields['mother'].queryset = product.mother.all()
            self.fields['ram'].queryset = product.ram.all()
            self.fields['storage'].queryset = product.storage.all()
            self.fields['graphics'].queryset = product.graphics.all()
            self.fields['operating_system'].queryset = product.operating_system.all()
            self.fields['screen_sizes'].queryset = product.screen_sizes.all()
            self.fields['screen_type'].queryset = product.screen_type.all()
            self.fields['screen_resolution'].queryset = product.screen_resolution.all()
            self.fields['touch_screen_touches'].queryset = product.touch_screen_touches.all()
            self.fields['formfactor'].queryset = product.formfactor.all()
            self.fields['webcam'].queryset = product.webcam.all()
            self.fields['keyset'].queryset = product.keyset.all()
            self.fields['keyboard_backlight'].queryset = product.keyboard_backlight.all()
            self.fields['power_supplies'].queryset = product.power_supplies.all()
            self.fields['sizes'].queryset = product.sizes.all()
            self.fields['controllers'].queryset = product.controllers.all()

class OrderCreateForm(forms.Form):
    delivery_address = forms.CharField(widget=forms.Textarea, required=True)

class ProductItemForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = '__all__'