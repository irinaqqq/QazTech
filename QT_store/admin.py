from django.contrib import admin
from .models import *

class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDescriptionInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Processor)
admin.site.register(OperatingSystem)
admin.site.register(Graphics)
admin.site.register(RAM)
admin.site.register(Storage)
admin.site.register(Port)