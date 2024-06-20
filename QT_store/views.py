from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import user_passes_test

def is_staff(user):
    return user.is_staff

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

    motherboards_by_line = defaultdict(lambda: defaultdict(list))
    for motherboard in product.mother.all():
        motherboards_by_line[motherboard.line][motherboard.type].append(motherboard.name)
    motherboards_by_line = {line: dict(sorted(types.items())) for line, types in motherboards_by_line.items()}

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
        'motherboards_by_line': motherboards_by_line,
    }
    return render(request, 'product_details.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def whowe(request):
    return render(request, 'whowe.html')

def partners_view(request):
    return render(request, 'partners.html')

def contactus(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('contactus')
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = FeedbackForm()
    return render(request, 'contactus.html', {'form': form})

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

def get_category_products(request):
    category_id = request.GET.get('category_id')
    try:
        category_products = Product.objects.filter(category_id=category_id)
        products_data = []
        for product in category_products:
            product_data = {
                'name': product.name,
                'features': product.features,  # Замените это на атрибуты продукта, которые вам нужны
                'url': product.get_absolute_url(),  # Предполагается, что у вас есть метод get_absolute_url в модели Product
            }
            # Если у вас есть модель ProductImage, получаем URL первого изображения продукта
            if product.images.exists():
                product_data['image_url'] = product.images.first().image.url
            else:
                product_data['image_url'] = ''  # По умолчанию, если изображения отсутствуют
            products_data.append(product_data)
        return JsonResponse({'products': products_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def lab(request):
    return render(request, 'lab.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@user_passes_test(is_staff, login_url='/')
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@user_passes_test(is_staff, login_url='/')
def dashboard(request):
    total_products = Product.objects.count()
    total_users = User.objects.count()
    context = {
        'total_products': total_products,
        'total_users': total_users,
    }
    return render(request, 'admin_templates/dashboard.html', context)

@user_passes_test(is_staff, login_url='/')
def feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_templates/feedbacks.html', {'feedbacks': feedbacks})

@user_passes_test(is_staff, login_url='/')
def orders(request):
    return render(request, 'admin_templates/orders.html')

@user_passes_test(is_staff, login_url='/')
def products(request):
    products = Product.objects.all()
    return render(request, 'admin_templates/products.html', {'products': products})

@user_passes_test(is_staff, login_url='/')
def requests(request):
    return render(request, 'admin_templates/requests.html')

@user_passes_test(is_staff, login_url='/')
def users(request):
    return render(request, 'admin_templates/users.html')

@user_passes_test(is_staff, login_url='/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save() 
            return redirect('products')
    else:
        form = ProductForm()
    
    return render(request, 'admin_templates/add_product.html', {'form': form})

@user_passes_test(is_staff, login_url='/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    
    return render(request, 'admin_templates/products.html', {'product': product})

@user_passes_test(is_staff, login_url='/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products') 
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin_templates/edit_product.html', {'form': form, 'product': product})