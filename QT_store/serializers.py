from rest_framework import serializers  
from .models import (Motherboard, ProcBrand, ProcLine, Processor, OperatingSystem, Graphics, RAM, Storage, Port,   
                     ScreenSize, PowerSupply, Controller, Size, KeyboardLight, ScreenResolution, FormFactor,   
                     KeyboardSet, TouchST, ScreenType, WebCam, Product, ProductImage, ProductDescription)  
  
class MotherboardSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Motherboard model.  
      
    Fields:  
    - id: Unique identifier for the motherboard.  
    - name: Name of the motherboard.  
    - chipset: Chipset used in the motherboard.  
    - socket: CPU socket type.  
    """  
    class Meta:  
        model = Motherboard  
        fields = '__all__'  
  
class ProcBrandSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ProcBrand model.  
      
    Fields:  
    - id: Unique identifier for the processor brand.  
    - name: Name of the processor brand.  
    """  
    class Meta:  
        model = ProcBrand  
        fields = '__all__'  
  
class ProcLineSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ProcLine model.  
      
    Fields:  
    - id: Unique identifier for the processor line.  
    - name: Name of the processor line.  
    - brand: Brand to which the processor line belongs.  
    """  
    class Meta:  
        model = ProcLine  
        fields = '__all__'  
  
class ProcessorSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Processor model.  
      
    Fields:  
    - id: Unique identifier for the processor.  
    - name: Name of the processor.  
    - brand: Brand of the processor.  
    - line: Line of the processor.  
    - cores: Number of cores in the processor.  
    - threads: Number of threads in the processor.  
    - base_clock: Base clock speed of the processor.  
    - boost_clock: Boost clock speed of the processor.  
    """  
    class Meta:  
        model = Processor  
        fields = '__all__'  
  
class OperatingSystemSerializer(serializers.ModelSerializer):  
    """  
    Serializer for OperatingSystem model.  
      
    Fields:  
    - id: Unique identifier for the operating system.  
    - name: Name of the operating system.  
    - version: Version of the operating system.  
    """  
    class Meta:  
        model = OperatingSystem  
        fields = '__all__'  
  
class GraphicsSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Graphics model.  
      
    Fields:  
    - id: Unique identifier for the graphics card.  
    - name: Name of the graphics card.  
    - memory: Amount of memory in the graphics card.  
    """  
    class Meta:  
        model = Graphics  
        fields = '__all__'  
  
class RAMSerializer(serializers.ModelSerializer):  
    """  
    Serializer for RAM model.  
      
    Fields:  
    - id: Unique identifier for the RAM.  
    - type: Type of the RAM (e.g., DDR4).  
    - size: Size of the RAM.  
    """  
    class Meta:  
        model = RAM  
        fields = '__all__'  
  
class StorageSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Storage model.  
      
    Fields:  
    - id: Unique identifier for the storage.  
    - type: Type of the storage (e.g., SSD, HDD).  
    - capacity: Capacity of the storage.  
    """  
    class Meta:  
        model = Storage  
        fields = '__all__'  
  
class PortSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Port model.  
      
    Fields:  
    - id: Unique identifier for the port.  
    - type: Type of the port (e.g., USB, HDMI).  
    - quantity: Quantity of the ports.  
    """  
    class Meta:  
        model = Port  
        fields = '__all__'  
  
class ScreenSizeSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ScreenSize model.  
      
    Fields:  
    - id: Unique identifier for the screen size.  
    - size: Size of the screen.  
    """  
    class Meta:  
        model = ScreenSize  
        fields = '__all__'  
  
class PowerSupplySerializer(serializers.ModelSerializer):  
    """  
    Serializer for PowerSupply model.  
      
    Fields:  
    - id: Unique identifier for the power supply.  
    - power: Power rating of the power supply.  
    """  
    class Meta:  
        model = PowerSupply  
        fields = '__all__'  
  
class ControllerSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Controller model.  
      
    Fields:  
    - id: Unique identifier for the controller.  
    - name: Name of the controller.  
    """  
    class Meta:  
        model = Controller  
        fields = '__all__'  
  
class SizeSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Size model.  
      
    Fields:  
    - id: Unique identifier for the size.  
    - dimensions: Dimensions of the size.  
    """  
    class Meta:  
        model = Size  
        fields = '__all__'  
  
class KeyboardLightSerializer(serializers.ModelSerializer):  
    """  
    Serializer for KeyboardLight model.  
      
    Fields:  
    - id: Unique identifier for the keyboard light.  
    - type: Type of the keyboard light (e.g., RGB, single color).  
    """  
    class Meta:  
        model = KeyboardLight  
        fields = '__all__'  
  
class ScreenResolutionSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ScreenResolution model.  
      
    Fields:  
    - id: Unique identifier for the screen resolution.  
    - resolution: Resolution of the screen.  
    """  
    class Meta:  
        model = ScreenResolution  
        fields = '__all__'  
  
class FormFactorSerializer(serializers.ModelSerializer):  
    """  
    Serializer for FormFactor model.  
      
    Fields:  
    - id: Unique identifier for the form factor.  
    - type: Type of the form factor (e.g., ATX, Micro-ATX).  
    """  
    class Meta:  
        model = FormFactor  
        fields = '__all__'  
  
class KeyboardSetSerializer(serializers.ModelSerializer):  
    """  
    Serializer for KeyboardSet model.  
      
    Fields:  
    - id: Unique identifier for the keyboard set.  
    - layout: Layout of the keyboard set (e.g., QWERTY, AZERTY).  
    """  
    class Meta:  
        model = KeyboardSet  
        fields = '__all__'  
  
class TouchSTSerializer(serializers.ModelSerializer):  
    """  
    Serializer for TouchST model.  
      
    Fields:  
    - id: Unique identifier for the touch screen technology.  
    - type: Type of the touch screen technology (e.g., capacitive, resistive).  
    """  
    class Meta:  
        model = TouchST  
        fields = '__all__'  
  
class ScreenTypeSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ScreenType model.  
      
    Fields:  
    - id: Unique identifier for the screen type.  
    - type: Type of the screen (e.g., LED, OLED).  
    """  
    class Meta:  
        model = ScreenType  
        fields = '__all__'  
  
class WebCamSerializer(serializers.ModelSerializer):  
    """  
    Serializer for WebCam model.  
      
    Fields:  
    - id: Unique identifier for the webcam.  
    - resolution: Resolution of the webcam.  
    """  
    class Meta:  
        model = WebCam  
        fields = '__all__'  
  
class ProductSerializer(serializers.ModelSerializer):  
    """  
    Serializer for Product model.  
      
    Fields:  
    - id: Unique identifier for the product.  
    - name: Name of the product.  
    - description: Description of the product.  
    - price: Price of the product.  
    - stock: Stock quantity of the product.  
    - created_at: Date when the product was created.  
    - updated_at: Date when the product was last updated.  
    """  
    class Meta:  
        model = Product  
        fields = '__all__'  
  
class ProductImageSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ProductImage model.  
      
    Fields:  
    - id: Unique identifier for the product image.  
    - product: Product to which the image belongs.  
    - image: Image file.  
    """  
    class Meta:  
        model = ProductImage  
        fields = '__all__'  
  
class ProductDescriptionSerializer(serializers.ModelSerializer):  
    """  
    Serializer for ProductDescription model.  
      
    Fields:  
    - id: Unique identifier for the product description.  
    - product: Product to which the description belongs.  
    - description: Detailed description of the product.  
    """  
    class Meta:  
        model = ProductDescription  
        fields = '__all__'  