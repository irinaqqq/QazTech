"""URL configuration for QT_website project.  
  
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
from django.urls import path, include  
from QT_store import views  
from django.contrib.auth import views as auth_views  
from rest_framework import permissions  
from drf_yasg.views import get_schema_view  
from drf_yasg import openapi  
  
# API views import  
from QT_store.views import (  
    MotherboardViewSet, ProcBrandViewSet, ProcLineViewSet, ProcessorViewSet, OperatingSystemViewSet,  
    GraphicsViewSet, RAMViewSet, StorageViewSet, PortViewSet, ScreenSizeViewSet, PowerSupplyViewSet,  
    ControllerViewSet, SizeViewSet, KeyboardLightViewSet, ScreenResolutionViewSet, FormFactorViewSet,  
    KeyboardSetViewSet, TouchSTViewSet, ScreenTypeViewSet, WebCamViewSet, ProductViewSet,  
    ProductImageViewSet, ProductDescriptionViewSet  
)  
from rest_framework.routers import DefaultRouter  
  
router = DefaultRouter()  
router.register(r'motherboards', MotherboardViewSet)  
router.register(r'proc-brands', ProcBrandViewSet)  
router.register(r'proc-lines', ProcLineViewSet)  
router.register(r'processors', ProcessorViewSet)  
router.register(r'operating-systems', OperatingSystemViewSet)  
router.register(r'graphics', GraphicsViewSet)  
router.register(r'rams', RAMViewSet)  
router.register(r'storages', StorageViewSet)  
router.register(r'ports', PortViewSet)  
router.register(r'screen-sizes', ScreenSizeViewSet)  
router.register(r'power-supplies', PowerSupplyViewSet)  
router.register(r'controllers', ControllerViewSet)  
router.register(r'sizes', SizeViewSet)  
router.register(r'keyboard-lights', KeyboardLightViewSet)  
router.register(r'screen-resolutions', ScreenResolutionViewSet)  
router.register(r'form-factors', FormFactorViewSet)  
router.register(r'keyboard-sets', KeyboardSetViewSet)  
router.register(r'touch-sts', TouchSTViewSet)  
router.register(r'screen-types', ScreenTypeViewSet)  
router.register(r'webcams', WebCamViewSet)  
router.register(r'products', ProductViewSet)  
router.register(r'product-images', ProductImageViewSet)  
router.register(r'product-descriptions', ProductDescriptionViewSet)  
  
schema_view = get_schema_view(  
   openapi.Info(  
      title="QT_website API",  
      default_version='v1',  
      description="API documentation for QT_website",  
      terms_of_service="https://www.google.com/policies/terms/",  
      contact=openapi.Contact(email="contact@yourproject.local"),  
      license=openapi.License(name="BSD License"),  
   ),  
   public=True,  
   permission_classes=(permissions.AllowAny,),  
)  
  
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
    path('cart/', views.cart, name='cart'),  
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),  
    path('order/create/', views.order_create, name='order_create'),  
    path('order/<int:order_id>/', views.user_order_details, name='user_order_details'),  
    path('get_category_products/', views.get_category_products, name='get_category_products'),  
    path('lab/', views.lab, name='lab'),  
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup_view, name='signup'),  
    path('profile/', views.profile_view, name='profile'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('commercial_offer/', views.commercial_offer, name='commercial_offer'),  
    path('commercial_request/<int:commercial_request_id>/', views.commercial_request_detail_user, name='commercial_request_detail_user'),  
    path('myadmin/dashboard/', views.dashboard, name='dashboard'),  
    path('myadmin/feedbacks/', views.feedbacks, name='feedbacks'),  
    path('myadmin/update_feedbacks_read_status/', views.update_feedbacks_read_status, name='update_feedbacks_read_status'),  
    path('myadmin/orders/', views.orders, name='orders'),  
    path('myadmin/update_order_status/', views.update_order_status, name='update_order_status'),  
    path('myadmin/order/<int:order_id>/', views.order_details, name='order_details'),  
    path('myadmin/order/<int:order_id>/approve/', views.approve_price, name='approve_price'),  
    path('myadmin/products/', views.products, name='products'),  
    path('myadmin/requests/', views.requests, name='requests'),  
    path('myadmin/users/', views.users, name='users'),  
    path('myadmin/edit/<int:pk>/', views.edit_product, name='edit_product'),  
    path('myadmin/add/', views.add_product, name='add_product'),  
    path('myadmin/delete/<int:pk>/', views.delete_product, name='delete_product'),  
    path('myadmin/approve_request/<int:request_id>/', views.approve_request, name='approve_request'),  
    path('myadmin/reject_request/<int:request_id>/', views.reject_request, name='reject_request'),  
    path('myadmin/commercial_requests/', views.commercial_requests_list, name='commercial_requests_list'),  
    path('myadmin/commercial_request/<int:commercial_request_id>/', views.commercial_request_detail, name='commercial_request_detail'),  
    path('commercial_request/document/<int:commercial_request_id>/', views.commercial_request_document, name='commercial_request_document'),  
    path('api/', include(router.urls)),  
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  
]  
  
# Добавьте обработку медиа-файлов  
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  
  
# Обработка статических файлов  
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  