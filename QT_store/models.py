from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=110, verbose_name="Описание(кратко)", null=True)
    image = models.ImageField(upload_to='static/category_images/', verbose_name="Фото", null=True)
    # Другие поля, если нужно
    def __str__(self):
        return self.name

class ProcBrand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Бренд", null=True, unique=True)

    def __str__(self):
        return self.name

class ProcLine(models.Model):
    brand = models.ForeignKey(ProcBrand, on_delete=models.CASCADE, verbose_name="Бренд", null=True)
    name = models.CharField(max_length=50, verbose_name="Линейка", null=True, unique=True)

    def __str__(self):
        return self.name

class Processor(models.Model):
    brand = models.ForeignKey(ProcBrand, on_delete=models.CASCADE, verbose_name="Бренд", null=True)
    line = models.ForeignKey(ProcLine, on_delete=models.CASCADE, verbose_name="Линейка", null=True)
    series = models.CharField(max_length=50, verbose_name="Серия", default='', null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, verbose_name="Процессор", editable=False)

    def save(self, *args, **kwargs):
        self.name = f"{self.brand} {self.line} {self.series}" if self.series else f"{self.brand} {self.line}"
        super().save(*args, **kwargs)

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
    SIZE_CHOICES = [
        ('4GB', '4 ГБ'),
        ('8GB', '8 ГБ'),
        ('16GB', '16 ГБ'),
        ('32GB', '32 ГБ'),
        ('64GB', '64 ГБ'),
        ('128GB', '128 ГБ'),
        ('256GB', '256 ГБ'),
        ('512GB', '512 ГБ'),
        ('1024GB', '1 ТБ'),
        ('1536GB', '1,5 ТБ'),
    ]

    TYPE_CHOICES = [
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]

    size = models.CharField(max_length=10, choices=SIZE_CHOICES, verbose_name="Объем оперативной памяти", null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип оперативной памяти", null=True)

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

    SIZE_CHOICES = [
        ('120GB', '120 ГБ'),
        ('240GB', '240 ГБ'),
        ('480GB', '480 ГБ'),
        ('500GB', '500 ГБ'),
        ('1TB', '1 ТБ'),
        ('2TB', '2 ТБ'),
        ('4TB', '4 ТБ'),
        ('8TB', '8 ТБ'),
        ('16TB', '16 ТБ'),
        ('32TB', '32 ТБ'),
        ('64TB', '64 ТБ'),
        ('128TB', '128 ТБ'),
        ('256TB', '256 ТБ'),
        ('512TB', '512 ТБ'),
        ('1024TB', '1024 ТБ'),
    ]

    size = models.CharField(max_length=6, choices=SIZE_CHOICES, verbose_name="Объем накопителя", null=True)
    type = models.CharField(max_length=4, choices=STORAGE_TYPE_CHOICES, default=SSD, verbose_name="Тип накопителя", null=True)
    
    class Meta:
        unique_together = ('size', 'type')

    def __str__(self):
        return f"{self.size} ({self.get_type_display()})"

class Motherboard(models.Model):
    
    TYPE_CHOICES = [
        ('SOCKET', 'Socket'),
        ('FCBGA', 'FCBGA'),
    ]
    line = models.CharField(max_length=50, verbose_name="Линейка", choices=TYPE_CHOICES, default='Socket')
    type = models.CharField(max_length=50, verbose_name="Тип разъема", unique=True)
    name = models.CharField(max_length=100, verbose_name="Название", editable=False)

    def save(self, *args, **kwargs):
        self.name = f"{self.line} {self.type}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Port(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название порта", unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    description = models.TextField(verbose_name="Описание")
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Вес", null=True)
    features = models.CharField(max_length=60, verbose_name="Особенности(кратко)", null=True)
    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, verbose_name="Процессор")
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.SET_NULL, null=True, verbose_name="Операционная система")
    graphics = models.ForeignKey(Graphics, on_delete=models.SET_NULL, null=True, verbose_name="Видеокарта")
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, verbose_name="Оперативная память")
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, verbose_name="Накопители")
    ports = models.ManyToManyField(Port, verbose_name="Порты и разъемы")
    operating_temperature = models.CharField(max_length=20, verbose_name="Температура эксплуатации", null=True)
    storage_temperature = models.CharField(max_length=20, verbose_name="Температура хранения", null=True)
    operating_humidity = models.CharField(max_length=20, verbose_name="Рабочая влажность", null=True)
    storage_humidity = models.CharField(max_length=20, verbose_name="Влажность хранения", null=True)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Продукт")
    image = models.ImageField(upload_to='static/product_images/', verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для {self.product.name}"


class ProductDescription(models.Model):
    product = models.ForeignKey(Product, related_name='descriptions', on_delete=models.CASCADE, verbose_name="Продукт")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    image = models.ImageField(upload_to='static/product_descriptions/', verbose_name="Фото", blank=True, null=True)
    text = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


