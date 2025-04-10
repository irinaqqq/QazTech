from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.decorators import user_passes_test
import random
import string
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.views.decorators.csrf import csrf_protect 
import os

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

    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('cart')
        else:
            print(form.errors)  # Выводим ошибки формы в консоль для отладки
    else:
        form = AddToCartForm(product=product)


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
        'form': form,
    }
    return render(request, 'product_details.html', context)

def aboutus(request):
    return render(request, 'aboutus.html')

def whowe(request):
    return render(request, 'whowe.html')

def partners_view(request):
    return render(request, 'partners.html')

@csrf_protect
def contactus(request):
    if request.method == 'POST':
        # Проверка honey pot поля
        if 'honeypot' in request.POST and request.POST['honeypot']:
            return HttpResponse(status=403)  # Возвращаем ошибку доступа, если поле honeypot заполнено

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

def signup_view(request):
    if request.method == 'POST':
        form = RegistrationRequestForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegistrationRequestForm()
    return render(request, 'signup.html', {'form': form})



@user_passes_test(is_staff, login_url='/login')
def dashboard(request):
    total_products = Product.objects.count()
    total_users = User.objects.count() - 1
    pending_requests = RegistrationRequest.objects.filter(status='pending').count()
    unread_feedbacks_count = Feedback.objects.filter(is_read=False).count()
    pending_orders_count = Order.objects.filter(status='pending_verification').count()

    context = {
        'total_products': total_products,
        'total_users': total_users,
        'pending_requests': pending_requests,
        'unread_feedbacks_count': unread_feedbacks_count,
        'pending_orders_count': pending_orders_count,
    }
    return render(request, 'admin_templates/dashboard.html', context)

@user_passes_test(is_staff, login_url='/')
def feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_templates/feedbacks.html', {'feedbacks': feedbacks})

@staff_member_required
def update_feedbacks_read_status(request):
    if request.method == 'POST':
        Feedback.objects.filter(is_read=False).update(is_read=True)
        return JsonResponse({'message': 'Статусы прочтения отзывов успешно обновлены.'})
    else:
        return JsonResponse({'error': 'Метод запроса не поддерживается.'}, status=405)

@user_passes_test(is_staff, login_url='/')
def orders(request):
    delivered_orders = Order.objects.filter(status='delivered').order_by('-created_at')
    other_orders = Order.objects.exclude(status='delivered').order_by('-created_at')
    
    context = {
        'delivered_orders': delivered_orders,
        'other_orders': other_orders
    }
    
    return render(request, 'admin_templates/orders.html', context)

@user_passes_test(is_staff, login_url='/')
def update_order_status(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = status
        order.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
@user_passes_test(is_staff, login_url='/')
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_templates/order_details.html', {'order': order})

@user_passes_test(is_staff, login_url='/')
def approve_price(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        for item in order.items.all():
            price = request.POST.get(f'price_{item.id}')
            print(f'Item ID: {item.id}, Posted price: {price}')
            if price:
                item.price = float(price)
                item.save()
        return redirect('order_details', order_id=order_id)
    else:
        return redirect('order_details', order_id=order_id)



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
                'organization': custom_data.organization,
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
            product = form.save()
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
        Custom.objects.create(user=user, phone_number=registration_request.phone_number, organization=registration_request.organization, initial_password=password)

        registration_request.status = 'approved'
        registration_request.save()

        try:
            send_mail(
                'Добро пожаловать на mytechnology.kz!',
                f'''
                Уважаемый(ая) {registration_request.first_name},

                Благодарим вас за регистрацию на сайте mytechnology.kz. Мы рады приветствовать вас на нашем сайте!

                Ваши учетные данные для входа:
                Логин: {registration_request.email}
                Пароль: {password}

                Теперь у вас есть возможность добавлять товары в корзину и совершать покупки, а также запрашивать коммерческие предложения, специально подобранные под ваши нужды.

                Если у вас возникнут какие-либо вопросы или вам потребуется помощь, пожалуйста, не стесняйтесь обращаться в нашу службу поддержки по адресу info@qt.com.kz. Мы всегда готовы помочь вам!

                Спасибо за то, что выбрали mytechnology.kz. Желаем вам приятных покупок!

                С уважением,
                Команда mytechnology.kz
                ''',
                'info@qt.com.kz',
                [registration_request.email],
                fail_silently=False,
            )
        except Exception as e:
            # Логирование ошибки или выполнение других действий
            print(f"Error sending email: {e}")
    return redirect('requests')

@staff_member_required
def reject_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, id=request_id)
    if registration_request.status == 'pending':
        registration_request.status = 'rejected'
        registration_request.save()
    return redirect('requests')


def clean_unused_images():
    """
    Deletes unused image files that are no longer associated with any `ProductImage` objects in the database,
    and prints out the names of these files along with a count of how many were deleted.
    """
    # Get all image files in the specified upload directory
    image_directory = os.path.join(settings.MEDIA_ROOT, 'product_images/')
    existing_images = set(os.listdir(image_directory))

    # Get all image paths currently associated with `ProductImage` objects in the database
    used_images = set(ProductImage.objects.values_list('image', flat=True))

    # Extract the filenames only, without the directory
    existing_image_names = set(os.path.basename(image) for image in existing_images)
    used_image_names = set(os.path.basename(image) for image in used_images)

    # Find unused images
    unused_images = existing_image_names - used_image_names

    # Delete unused images
    for unused_image in unused_images:
        image_path = os.path.join(image_directory, unused_image)
        try:
            os.remove(image_path)
            print(f"Deleted: {image_path}")
        except OSError as e:
            print(f"Error deleting {image_path}: {e}")

    print(f"Count of unused images deleted: {len(unused_images)}")


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart') 

@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                delivery_address=form.cleaned_data['delivery_address']
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    note=item.note,
                    processor=item.processor,
                    mother=item.mother,
                    ram=item.ram,
                    storage=item.storage,
                    graphics=item.graphics,
                    operating_system=item.operating_system,
                    screen_sizes=item.screen_sizes,
                    screen_type=item.screen_type,
                    screen_resolution=item.screen_resolution,
                    touch_screen_touches=item.touch_screen_touches,
                    formfactor=item.formfactor,
                    webcam=item.webcam,
                    keyset=item.keyset,
                    keyboard_backlight=item.keyboard_backlight,
                    power_supplies=item.power_supplies,
                    sizes=item.sizes,
                    controllers=item.controllers
                )
            # Очистить корзину
            cart_items.delete()
            return redirect('profile')
    else:
        form = OrderCreateForm()
    
    return render(request, 'order_create.html', {'cart_items': cart_items, 'form': form})

@login_required
def user_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'user_order_detail.html', {'order': order, 'order_items': order_items})

@login_required
def commercial_offer(request):
    ProductItemFormSet = inlineformset_factory(
        CommercialRequest,
        ProductItem,
        form=ProductItemForm, 
        fields='__all__',
        extra=1,
        can_delete=True,
    )
    
    if request.method == 'POST':
        formset = ProductItemFormSet(request.POST, request.FILES, instance=None)
        
        if formset.is_valid():
            # Создание объекта CommercialRequest
            commercial_request = CommercialRequest.objects.create(user=request.user)
            
            # Сохранение всех объектов ProductItem
            instances = formset.save(commit=False)
            
            # Установка связи и сохранение
            for instance in instances:
                instance.commercial_request = commercial_request
                instance.save()

            # Сохранение ManyToMany полей после всех сохранений
            formset.save_m2m()
            
            return redirect('profile')

    else:
        formset = ProductItemFormSet(instance=None)

    return render(request, 'commercial_offer.html', {'formset': formset})

@staff_member_required
def commercial_requests_list(request):
    commercial_requests = CommercialRequest.objects.all()
    return render(request, 'admin_templates/commercial_requests_list.html', {'commercial_requests': commercial_requests})

@staff_member_required
def commercial_request_detail(request, commercial_request_id):
    commercial_request = get_object_or_404(CommercialRequest, pk=commercial_request_id)
    product_items = commercial_request.product_items.all()

    if request.method == 'POST':
        for product_item in product_items:
            product_item_id = request.POST.get(f'product_item_id_{product_item.id}')
            if product_item_id:
                price = request.POST.get(f'price_{product_item.id}')
                product_item.price = Decimal(price)
                print(product_item.price)
                print(product_item.quantity)
                product_item.total_price = product_item.price * product_item.quantity
                print(product_item.total_price)
                product_item.save()
                
        return redirect('commercial_request_detail', commercial_request_id=commercial_request_id)

    context = {
        'commercial_request': commercial_request,
        'product_items': product_items,
    }
    return render(request, 'admin_templates/commercial_request_detail.html', context)


@login_required
def commercial_request_document(request, commercial_request_id):
    commercial_request = get_object_or_404(CommercialRequest, pk=commercial_request_id)
    product_items = commercial_request.product_items.all()
    if commercial_request.user != request.user and not request.user.is_staff:
        raise PermissionDenied("У вас нет доступа к этому документу.")

    context = {
        'commercial_request': commercial_request,
        'product_items': product_items,
    }
    return render(request, 'admin_templates/commercial_request_document.html', context)

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    commercial_requests = CommercialRequest.objects.filter(user=request.user).order_by('-created_at')
    try:
        custom_profile = Custom.objects.get(user=request.user)
    except ObjectDoesNotExist:
        custom_profile = None

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user) 
            return redirect('profile') 
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'user': request.user,
        'custom_profile': custom_profile,
        'password_form': password_form,
        'orders': orders,
        'commercial_requests': commercial_requests
    })

@login_required
def commercial_request_detail_user(request, commercial_request_id):
    commercial_request = get_object_or_404(CommercialRequest, pk=commercial_request_id)
    product_items = commercial_request.product_items.all()
    if commercial_request.user != request.user:
        raise PermissionDenied("Вы не имеете доступа к этому запросу.")
    context = {
        'commercial_request': commercial_request,
        'product_items': product_items,
    }
    return render(request, 'commercial_request_detail_user.html', context)

from rest_framework import viewsets  
from .models import (Motherboard, ProcBrand, ProcLine, Processor, OperatingSystem, Graphics, RAM, Storage, Port,   
                     ScreenSize, PowerSupply, Controller, Size, KeyboardLight, ScreenResolution, FormFactor,   
                     KeyboardSet, TouchST, ScreenType, WebCam, Product, ProductImage, ProductDescription)  
from .serializers import (MotherboardSerializer, ProcBrandSerializer, ProcLineSerializer, ProcessorSerializer,   
                          OperatingSystemSerializer, GraphicsSerializer, RAMSerializer, StorageSerializer,   
                          PortSerializer, ScreenSizeSerializer, PowerSupplySerializer, ControllerSerializer,   
                          SizeSerializer, KeyboardLightSerializer, ScreenResolutionSerializer, FormFactorSerializer,   
                          KeyboardSetSerializer, TouchSTSerializer, ScreenTypeSerializer, WebCamSerializer,   
                          ProductSerializer, ProductImageSerializer, ProductDescriptionSerializer)  
  
class MotherboardViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given motherboard.  
  
    list:  
    Return a list of all the existing motherboards.  
  
    create:  
    Create a new motherboard instance.  
  
    update:  
    Update the given motherboard.  
  
    partial_update:  
    Partially update the given motherboard.  
  
    delete:  
    Delete the given motherboard.  
    """  
    queryset = Motherboard.objects.all()  
    serializer_class = MotherboardSerializer  
  
class ProcBrandViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given processor brand.  
  
    list:  
    Return a list of all the existing processor brands.  
  
    create:  
    Create a new processor brand instance.  
  
    update:  
    Update the given processor brand.  
  
    partial_update:  
    Partially update the given processor brand.  
  
    delete:  
    Delete the given processor brand.  
    """  
    queryset = ProcBrand.objects.all()  
    serializer_class = ProcBrandSerializer  
  
class ProcLineViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given processor line.  
  
    list:  
    Return a list of all the existing processor lines.  
  
    create:  
    Create a new processor line instance.  
  
    update:  
    Update the given processor line.  
  
    partial_update:  
    Partially update the given processor line.  
  
    delete:  
    Delete the given processor line.  
    """  
    queryset = ProcLine.objects.all()  
    serializer_class = ProcLineSerializer  
  
class ProcessorViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given processor.  
  
    list:  
    Return a list of all the existing processors.  
  
    create:  
    Create a new processor instance.  
  
    update:  
    Update the given processor.  
  
    partial_update:  
    Partially update the given processor.  
  
    delete:  
    Delete the given processor.  
    """  
    queryset = Processor.objects.all()  
    serializer_class = ProcessorSerializer  
  
class OperatingSystemViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given operating system.  
  
    list:  
    Return a list of all the existing operating systems.  
  
    create:  
    Create a new operating system instance.  
  
    update:  
    Update the given operating system.  
  
    partial_update:  
    Partially update the given operating system.  
  
    delete:  
    Delete the given operating system.  
    """  
    queryset = OperatingSystem.objects.all()  
    serializer_class = OperatingSystemSerializer  
  
class GraphicsViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given graphics card.  
  
    list:  
    Return a list of all the existing graphics cards.  
  
    create:  
    Create a new graphics card instance.  
  
    update:  
    Update the given graphics card.  
  
    partial_update:  
    Partially update the given graphics card.  
  
    delete:  
    Delete the given graphics card.  
    """  
    queryset = Graphics.objects.all()  
    serializer_class = GraphicsSerializer  
  
class RAMViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given RAM.  
  
    list:  
    Return a list of all the existing RAMs.  
  
    create:  
    Create a new RAM instance.  
  
    update:  
    Update the given RAM.  
  
    partial_update:  
    Partially update the given RAM.  
  
    delete:  
    Delete the given RAM.  
    """  
    queryset = RAM.objects.all()  
    serializer_class = RAMSerializer  
  
class StorageViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given storage.  
  
    list:  
    Return a list of all the existing storages.  
  
    create:  
    Create a new storage instance.  
  
    update:  
    Update the given storage.  
  
    partial_update:  
    Partially update the given storage.  
  
    delete:  
    Delete the given storage.  
    """  
    queryset = Storage.objects.all()  
    serializer_class = StorageSerializer  
  
class PortViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given port.  
  
    list:  
    Return a list of all the existing ports.  
  
    create:  
    Create a new port instance.  
  
    update:  
    Update the given port.  
  
    partial_update:  
    Partially update the given port.  
  
    delete:  
    Delete the given port.  
    """  
    queryset = Port.objects.all()  
    serializer_class = PortSerializer  
  
class ScreenSizeViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given screen size.  
  
    list:  
    Return a list of all the existing screen sizes.  
  
    create:  
    Create a new screen size instance.  
  
    update:  
    Update the given screen size.  
  
    partial_update:  
    Partially update the given screen size.  
  
    delete:  
    Delete the given screen size.  
    """  
    queryset = ScreenSize.objects.all()  
    serializer_class = ScreenSizeSerializer  
  
class PowerSupplyViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given power supply.  
  
    list:  
    Return a list of all the existing power supplies.  
  
    create:  
    Create a new power supply instance.  
  
    update:  
    Update the given power supply.  
  
    partial_update:  
    Partially update the given power supply.  
  
    delete:  
    Delete the given power supply.  
    """  
    queryset = PowerSupply.objects.all()  
    serializer_class = PowerSupplySerializer  
  
class ControllerViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given controller.  
  
    list:  
    Return a list of all the existing controllers.  
  
    create:  
    Create a new controller instance.  
  
    update:  
    Update the given controller.  
  
    partial_update:  
    Partially update the given controller.  
  
    delete:  
    Delete the given controller.  
    """  
    queryset = Controller.objects.all()  
    serializer_class = ControllerSerializer  
  
class SizeViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given size.  
  
    list:  
    Return a list of all the existing sizes.  
  
    create:  
    Create a new size instance.  
  
    update:  
    Update the given size.  
  
    partial_update:  
    Partially update the given size.  
  
    delete:  
    Delete the given size.  
    """  
    queryset = Size.objects.all()  
    serializer_class = SizeSerializer  
  
class KeyboardLightViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given keyboard light.  
  
    list:  
    Return a list of all the existing keyboard lights.  
  
    create:  
    Create a new keyboard light instance.  
  
    update:  
    Update the given keyboard light.  
  
    partial_update:  
    Partially update the given keyboard light.  
  
    delete:  
    Delete the given keyboard light.  
    """  
    queryset = KeyboardLight.objects.all()  
    serializer_class = KeyboardLightSerializer  
  
class ScreenResolutionViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given screen resolution.  
  
    list:  
    Return a list of all the existing screen resolutions.  
  
    create:  
    Create a new screen resolution instance.  
  
    update:  
    Update the given screen resolution.  
  
    partial_update:  
    Partially update the given screen resolution.  
  
    delete:  
    Delete the given screen resolution.  
    """  
    queryset = ScreenResolution.objects.all()  
    serializer_class = ScreenResolutionSerializer  
  
class FormFactorViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given form factor.  
  
    list:  
    Return a list of all the existing form factors.  
  
    create:  
    Create a new form factor instance.  
  
    update:  
    Update the given form factor.  
  
    partial_update:  
    Partially update the given form factor.  
  
    delete:  
    Delete the given form factor.  
    """  
    queryset = FormFactor.objects.all()  
    serializer_class = FormFactorSerializer  
  
class KeyboardSetViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given keyboard set.  
  
    list:  
    Return a list of all the existing keyboard sets.  
  
    create:  
    Create a new keyboard set instance.  
  
    update:  
    Update the given keyboard set.  
  
    partial_update:  
    Partially update the given keyboard set.  
  
    delete:  
    Delete the given keyboard set.  
    """  
    queryset = KeyboardSet.objects.all()  
    serializer_class = KeyboardSetSerializer  
  
class TouchSTViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given touch screen technology.  
  
    list:  
    Return a list of all the existing touch screen technologies.  
  
    create:  
    Create a new touch screen technology instance.  
  
    update:  
    Update the given touch screen technology.  
  
    partial_update:  
    Partially update the given touch screen technology.  
  
    delete:  
    Delete the given touch screen technology.  
    """  
    queryset = TouchST.objects.all()  
    serializer_class = TouchSTSerializer  
  
class ScreenTypeViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given screen type.  
  
    list:  
    Return a list of all the existing screen types.  
  
    create:  
    Create a new screen type instance.  
  
    update:  
    Update the given screen type.  
  
    partial_update:  
    Partially update the given screen type.  
  
    delete:  
    Delete the given screen type.  
    """  
    queryset = ScreenType.objects.all()  
    serializer_class = ScreenTypeSerializer  
  
class WebCamViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given webcam.  
  
    list:  
    Return a list of all the existing webcams.  
  
    create:  
    Create a new webcam instance.  
  
    update:  
    Update the given webcam.  
  
    partial_update:  
    Partially update the given webcam.  
  
    delete:  
    Delete the given webcam.  
    """  
    queryset = WebCam.objects.all()  
    serializer_class = WebCamSerializer  
  
class ProductViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given product.  
  
    list:  
    Return a list of all the existing products.  
  
    create:  
    Create a new product instance.  
  
    update:  
    Update the given product.  
  
    partial_update:  
    Partially update the given product.  
  
    delete:  
    Delete the given product.  
    """  
    queryset = Product.objects.all()  
    serializer_class = ProductSerializer  
  
class ProductImageViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given product image.  
  
    list:  
    Return a list of all the existing product images.  
  
    create:  
    Create a new product image instance.  
  
    update:  
    Update the given product image.  
  
    partial_update:  
    Partially update the given product image.  
  
    delete:  
    Delete the given product image.  
    """  
    queryset = ProductImage.objects.all()  
    serializer_class = ProductImageSerializer  
  
class ProductDescriptionViewSet(viewsets.ModelViewSet):  
    """  
    retrieve:  
    Return the given product description.  
  
    list:  
    Return a list of all the existing product descriptions.  
  
    create:  
    Create a new product description instance.  
  
    update:  
    Update the given product description.  
  
    partial_update:  
    Partially update the given product description.  
  
    delete:  
    Delete the given product description.  
    """  
    queryset = ProductDescription.objects.all()  
    serializer_class = ProductDescriptionSerializer