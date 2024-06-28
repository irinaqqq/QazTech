from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import user_passes_test
import random
import string

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
                if user.is_superuser:
                    return redirect('dashboard')  # Перенаправляем администратора на другую страницу
                else:
                    return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@user_passes_test(is_staff, login_url='/')
def signup_view(request):
    return render(request, 'signup.html')



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
    registration_requests = RegistrationRequest.objects.filter(status='pending')
    return render(request, 'admin_templates/requests.html', {'requests': registration_requests})

@user_passes_test(is_staff, login_url='/')
def users(request):
    all_users = User.objects.all()
    users_with_data = []

    for user in all_users:
        # Находим соответствующий объект Custom для каждого пользователя
        custom_data = Custom.objects.filter(user=user).first()

        if custom_data:
            users_with_data.append({
                'user': user,
                'initial_password': custom_data.initial_password,
                'phone_number': custom_data.phone_number,
            })
        # else:
        #     users_with_data.append({
        #         'user': user,
        #         'initial_password': '',
        #         'phone_number': '   ',
        #     })

    return render(request, 'admin_templates/users.html', {'users_with_data': users_with_data})


@user_passes_test(is_staff, login_url='/')
def add_product(request):
    ImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1, can_delete=True)
    DescriptionFormSet = inlineformset_factory(Product, ProductDescription, form=ProductDescriptionForm, extra=1, can_delete=True)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=Product())
        description_formset = DescriptionFormSet(request.POST, request.FILES, instance=Product())

        if form.is_valid() and image_formset.is_valid() and description_formset.is_valid():
            product = form.save(commit=False)

            # Проверяем и обрабатываем поля с температурой и влажностью
            fields_to_check = ['features','operating_temperature', 'storage_temperature', 'operating_humidity', 'storage_humidity']
            for field_name in fields_to_check:
                if getattr(product, field_name) is None:
                    setattr(product, field_name, '')

            product.save()

            instances = image_formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()

            description_formset.instance = product
            description_formset.save()

            return redirect('products')  # Перенаправление на страницу списка продуктов
    else:
        form = ProductForm()
        image_formset = ImageFormSet(instance=Product())
        description_formset = DescriptionFormSet(instance=Product())

    return render(request, 'admin_templates/add_product.html', {
        'form': form,
        'image_formset': image_formset,
        'description_formset': description_formset,
    })

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
    ImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=1, can_delete=True)
    DescriptionFormSet = inlineformset_factory(Product, ProductDescription, form=ProductDescriptionForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=product)
        description_formset = DescriptionFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and image_formset.is_valid() and description_formset.is_valid():
            product = form.save()  # Save the main product form
            
            fields_to_check = ['features','operating_temperature', 'storage_temperature', 'operating_humidity', 'storage_humidity']
            for field_name in fields_to_check:
                if getattr(product, field_name) is None:
                    setattr(product, field_name, '')

            product.save()

            # Сохраняем изображения и обрабатываем удаление
            for form in image_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            
            image_instances = image_formset.save(commit=False)
            for instance in image_instances:
                instance.product = product
                instance.save()
            
            # Сохраняем описания товара и обрабатываем удаление
            for form in description_formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            
            description_formset.save()

            return redirect('products')
        else:
            # Отображаем ошибки форм и формсетов для отладки
            print("form bug")
            print(form.errors)
            print("image bug")
            print(image_formset.errors)
            print("desc bug")
            print(description_formset.errors)
    else:
        form = ProductForm(instance=product)
        image_formset = ImageFormSet(instance=product)
        description_formset = DescriptionFormSet(instance=product)

    return render(request, 'admin_templates/edit_product.html', {
        'form': form,
        'image_formset': image_formset,
        'description_formset': description_formset,
        'product': product,
    })


@staff_member_required
def approve_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, id=request_id)
    if registration_request.status == 'pending':
        # Генерация случайного пароля
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create_user(
            username=registration_request.email,
            email=registration_request.email,
            password=password,
            first_name=registration_request.first_name,
            last_name=registration_request.last_name
        )
        # Создание объекта Custom с номером телефона и начальным паролем
        Custom.objects.create(user=user, phone_number=registration_request.phone_number, initial_password=password)

        registration_request.status = 'approved'
        registration_request.save()
        # Отправка email (позже добавить)
        # send_mail('Your Account Details', f'Your password is {password}', 'from@example.com', [registration_request.email])
    return redirect('requests')

@staff_member_required
def reject_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, id=request_id)
    if registration_request.status == 'pending':
        registration_request.status = 'rejected'
        registration_request.save()
    return redirect('requests')



from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

def clean_unused_images():
    """
    Cleans up image files that are no longer associated with any `ProductImage` objects in the database.
    """
    from django.db.models import F

    # Get all image files in the specified upload directory
    image_directory = os.path.join(settings.MEDIA_ROOT, 'product_images/')
    existing_images = set(os.listdir(image_directory))

    # Get all image paths currently associated with `ProductImage` objects in the database
    used_images = set(ProductImage.objects.values_list('image', flat=True))

    # Determine images in the directory that are not in use
    unused_images = existing_images - used_images

    # Delete unused image files from the filesystem
    for image_filename in unused_images:
        image_path = os.path.join(image_directory, image_filename)
        if os.path.isfile(image_path):
            os.remove(image_path)
            print(f"Deleted unused image file: {image_path}")
