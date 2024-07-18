from django.contrib import admin
from .models import *

class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDescriptionInline, ProductImageInline]

class CustomAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'initial_password')

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Processor)
admin.site.register(OperatingSystem)
admin.site.register(Graphics)
admin.site.register(RAM)
admin.site.register(Storage)
admin.site.register(Port)
admin.site.register(ProcLine)
admin.site.register(ProcBrand)
admin.site.register(Motherboard)
admin.site.register(ScreenSize)
admin.site.register(PowerSupply)
admin.site.register(Size)
admin.site.register(FormFactor)
admin.site.register(KeyboardSet)
admin.site.register(TouchST)
admin.site.register(Controller)
admin.site.register(ScreenType)
admin.site.register(WebCam)
admin.site.register(RegistrationRequest)
admin.site.register(Custom, CustomAdmin)
admin.site.register(Feedback)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(ProductItem)
admin.site.register(CommercialRequest)
admin.site.register(Order)
