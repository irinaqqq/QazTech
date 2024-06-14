"""
URL configuration for QT_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from QT_store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    path('about/', views.aboutus, name='aboutus'),
    path('whowe/', views.whowe, name='whowe'),
    path('partners/', views.partners_view, name='partners'),
    path('contact/', views.contactus, name='contactus'),
    path('faq/', views.faq, name='faq'),
    path('map/', views.map, name='map'),
    path('news/', views.news, name='news'),
    path('support/', views.support, name='support'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('get_category_products/', views.get_category_products, name='get_category_products'),
    path('lab/', views.lab, name='lab'),
    
] 

# Добавьте обработку медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработка статических файлов
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)