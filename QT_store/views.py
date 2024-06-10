from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q
from collections import defaultdict

def home(request):
    return render(request, 'home.html')

def categories(request):
    return render(request, 'categories.html')

def category_products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_products.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    descriptions = product.descriptions.all()
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5] 

    processors_by_brand = defaultdict(lambda: defaultdict(list))
    for processor in product.processor.all():
        processors_by_brand[processor.brand.name][processor.line.name].append(processor.series or '')
    processors_by_brand = {brand: dict(lines) for brand, lines in processors_by_brand.items()}

    ram_by_type = defaultdict(list)
    for ram in product.ram.all():
        if ram.size is not None:
            ram_by_type[ram.type].append(ram.size)
    ram_by_type = {ram_type: sorted(sizes, key=lambda x: int(x)) for ram_type, sizes in ram_by_type.items()}

    all_ram_sizes = [int(size) for sizes in ram_by_type.values() for size in sizes if size is not None]
    min_ram_size = min(all_ram_sizes) if all_ram_sizes else None
    max_ram_size = max(all_ram_sizes) if all_ram_sizes else None

    storage_by_type = defaultdict(list)
    for storage in product.storage.all():
        if storage.size is not None:
            storage_by_type[storage.type].append(storage.size)
    storage_by_type = {storage_type: sorted(sizes, key=lambda x: int(x)) for storage_type, sizes in storage_by_type.items()}

    formatted_storage_by_type = {}
    for storage_type, sizes in storage_by_type.items():
        formatted_sizes = []
        for size in sizes:
            if size is not None:
                size_int = int(size)
                unit = "TB" if size_int >= 1024 else "GB"
                formatted_sizes.append((size_int / 1024 if unit == "TB" else size_int, unit))
        formatted_storage_by_type[storage_type] = formatted_sizes

    all_sizes = [int(size) for sizes in storage_by_type.values() for size in sizes if size is not None]
    min_storage_size = min(all_sizes) if all_sizes else None
    max_storage_size = max(all_sizes) if all_sizes else None
    min_storage_unit = "GB"
    max_storage_unit = "GB"
    if min_storage_size is not None and min_storage_size >= 1024:
        min_storage_size = min_storage_size / 1024
        min_storage_unit = "TB"
    if max_storage_size is not None and max_storage_size >= 1024:
        max_storage_size = max_storage_size / 1024
        max_storage_unit = "TB"

    context = {
        'product': product,
        'similar_products': similar_products,
        'descriptions': descriptions,
        'processors_by_brand': processors_by_brand,
        'ram_by_type': ram_by_type,
        'storage_by_type': storage_by_type,
        'min_ram_size': min_ram_size,
        'max_ram_size': max_ram_size,
        'min_storage_size': min_storage_size,
        'max_storage_size': max_storage_size,
        'min_storage_unit': min_storage_unit,
        'max_storage_unit': max_storage_unit,
        'formatted_storage_by_type': formatted_storage_by_type,
    }
    return render(request, 'product_details.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def whowe(request):
    return render(request, 'whowe.html')

def partners_view(request):
    return render(request, 'partners.html')

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

def search(request):
    query = request.GET.get('q')
    if query:
        # Ищем продукты по названию или описанию
        result_products = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)
    else:
        result_products = []
    
    context = {
        'query': query,
        'result_products': result_products,
    }
    return render(request, 'search_results.html', context)