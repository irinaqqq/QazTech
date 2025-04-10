from rest_framework import serializers  
from .models import (  
    Motherboard, ProcBrand, ProcLine, Processor, OperatingSystem, Graphics, RAM, Storage, Port, ScreenSize,  
    PowerSupply, Controller, Size, KeyboardLight, ScreenResolution, FormFactor, KeyboardSet, TouchST,  
    ScreenType, WebCam, Product, ProductImage, ProductDescription  
)  
  
class MotherboardSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Motherboard  
        fields = '__all__'  
  
class ProcBrandSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ProcBrand  
        fields = '__all__'  
  
class ProcLineSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ProcLine  
        fields = '__all__'  
  
class ProcessorSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Processor  
        fields = '__all__'  
  
class OperatingSystemSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = OperatingSystem  
        fields = '__all__'  
  
class GraphicsSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Graphics  
        fields = '__all__'  
  
class RAMSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = RAM  
        fields = '__all__'  
  
class StorageSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Storage  
        fields = '__all__'  
  
class PortSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Port  
        fields = '__all__'  
  
class ScreenSizeSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ScreenSize  
        fields = '__all__'  
  
class PowerSupplySerializer(serializers.ModelSerializer):  
    class Meta:  
        model = PowerSupply  
        fields = '__all__'  
  
class ControllerSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Controller  
        fields = '__all__'  
  
class SizeSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Size  
        fields = '__all__'  
  
class KeyboardLightSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = KeyboardLight  
        fields = '__all__'  
  
class ScreenResolutionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ScreenResolution  
        fields = '__all__'  
  
class FormFactorSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = FormFactor  
        fields = '__all__'  
  
class KeyboardSetSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = KeyboardSet  
        fields = '__all__'  
  
class TouchSTSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = TouchST  
        fields = '__all__'  
  
class ScreenTypeSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ScreenType  
        fields = '__all__'  
  
class WebCamSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = WebCam  
        fields = '__all__'  
  
class ProductSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Product  
        fields = '__all__'  
  
class ProductImageSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ProductImage  
        fields = '__all__'  
  
class ProductDescriptionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = ProductDescription  
        fields = '__all__'  