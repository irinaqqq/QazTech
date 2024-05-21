from django.shortcuts import render, get_object_or_404
from .models import *

def home(request):
    return render(request, 'home.html')

def category_products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    descriptions = product.descriptions.all()
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5] 
    return render(request, 'product_details.html', {'product': product, 'similar_products' : similar_products,  'descriptions': descriptions})

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')

def faq(request):
    return render(request, 'faq.html')

def map(request):
    return render(request, 'map.html')

def news(request):
    return render(request, 'news.html')

def support(request):
    return render(request, 'support.html')