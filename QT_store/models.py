from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Другие поля, если нужно

class Processor(models.Model):
    name = models.CharField(max_length=255, verbose_name="Процессор")

    def __str__(self):
        return self.name

class OperatingSystem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Операционная система")

    def __str__(self):
        return self.name

class Graphics(models.Model):
    name = models.CharField(max_length=255, verbose_name="Видеокарта")

    def __str__(self):
        return self.name

class RAM(models.Model):
    size = models.CharField(max_length=255, verbose_name="Объем оперативной памяти")
    type = models.CharField(max_length=255, verbose_name="Тип оперативной памяти")

    def __str__(self):
        return f"{self.size} ({self.type})"

class Storage(models.Model):
    HDD = 'HDD'
    SSD = 'SSD'
    NVME = 'NVMe'
    
    STORAGE_TYPE_CHOICES = [
        (HDD, 'Hard Disk Drive (HDD)'),
        (SSD, 'Solid-State Drive (SSD)'),
        (NVME, 'Non-Volatile Memory Express (NVMe)'),
    ]

    size = models.CharField(max_length=255, verbose_name="Объем накопителя")
    type = models.CharField(max_length=4, choices=STORAGE_TYPE_CHOICES, default=SSD, verbose_name="Тип накопителя")

    def __str__(self):
        return f"{self.size} ({self.get_type_display()})"


class Port(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название порта")

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Вес", null=True)
    features = models.TextField(verbose_name="Особенности", null=True)
    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, verbose_name="Процессор")
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.SET_NULL, null=True, verbose_name="Операционная система")
    graphics = models.ForeignKey(Graphics, on_delete=models.SET_NULL, null=True, verbose_name="Видеокарта")
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, verbose_name="Оперативная память")
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, verbose_name="Накопители")
    ports = models.ManyToManyField(Port, verbose_name="Порты и разъемы")


class ProductDescription(models.Model):
    product = models.ForeignKey(Product, related_name='descriptions', on_delete=models.CASCADE, verbose_name="Продукт")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField(upload_to='product_descriptions/', verbose_name="Фото", blank=True, null=True)
    text = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


