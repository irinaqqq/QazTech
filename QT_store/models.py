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

class ScreenSize(models.Model):
    size = models.CharField(max_length=50, verbose_name="Размер экрана")

    def __str__(self):
        return self.size

class PowerSupply(models.Model):
    power = models.CharField(max_length=100, verbose_name="Мощность")


    def __str__(self):
        return self.power

class Controller(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    def __str__(self):
        return self.name

class Product(models.Model):
    DISCRETE_GRAPHICS_CHOICES = [
        (None, 'Нет'),
        (2, '2GB'),
        (4, '4GB'),
        (8, '8GB'),
        (16, '16GB'),
        (24, '24GB'),
    ]
    SCREEN_TYPE_CHOICES = [
        (None, 'Нет'),
        ('IPS', 'IPS'),
        ('VA', 'VA'),
        ('TN', 'TN'),
        ('PLS', 'PLS'),
        ('LED', 'LED'),
    ]
    
    WEBCAM_CHOICES = [
        (None, 'Нет'),
        (False, 'Без встроенной вебкамеры'),
        (True, 'Со встроенной веб камерой'),
    ]
    KEYBOARD_TYPE_CHOICES = [
        (None, 'Нет'),
        ('Wired', 'Проводная'),
        ('Wireless', 'Беспроводная'),
    ]
    KEYBOARD_BACKLIGHT_CHOICES = [
        (None, 'Нет'),
        (False, 'Без подсветки'),
        (True, 'С подсветкой'),
    ]
    TOUCH_SCREEN_CHOICES = [
        (True, 'Да'),
        (False, 'Нет'),
    ]
    SCREEN_RESOLUTION_CHOICES = [
        (None, 'Нет'),
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('Quad HD', 'Quad HD'),
        ('4K', '4K'),
        ('Ultra HD+', 'Ultra HD+'),
    ]

    FORM_FACTOR_CHOICES = [
        (None, 'Нет'),
        ('Horizontal', 'Горизонтальный'),
        ('Vertical', 'Вертикальный'),
    ]
    

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Вес", null=True, blank=True)
    features = models.CharField(max_length=60, verbose_name="Особенности(кратко)", null=True)
    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, verbose_name="Процессор", blank=True)
    operating_system = models.ForeignKey(OperatingSystem, on_delete=models.SET_NULL, null=True, verbose_name="Операционная система", blank=True)
    # graphics = models.ForeignKey(Graphics, on_delete=models.SET_NULL, null=True, verbose_name="Видеокарта", blank=True)
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, verbose_name="Оперативная память", blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, verbose_name="Накопители", blank=True)
    ports = models.ManyToManyField(Port, verbose_name="Порты и разъемы", blank=True)
    operating_temperature = models.CharField(max_length=20, verbose_name="Температура эксплуатации", null=True, blank=True)
    storage_temperature = models.CharField(max_length=20, verbose_name="Температура хранения", null=True, blank=True)
    operating_humidity = models.CharField(max_length=20, verbose_name="Рабочая влажность", null=True, blank=True)
    storage_humidity = models.CharField(max_length=20, verbose_name="Влажность хранения", null=True, blank=True)

    screen_type = models.CharField(max_length=50, verbose_name="Тип экрана", choices=SCREEN_TYPE_CHOICES, blank=True, null=True)
    webcam = models.CharField(max_length=20, verbose_name="Веб камера", choices=WEBCAM_CHOICES, default=None, blank=True,)
    discrete_graphics = models.IntegerField(verbose_name="Видеокарта дискретная", choices=DISCRETE_GRAPHICS_CHOICES, blank=True, null=True)
    keyboard_type = models.CharField(max_length=50, verbose_name="Комплект клавиатура и мышь", choices=KEYBOARD_TYPE_CHOICES, blank=True, null=True)
    keyboard_backlight = models.CharField(max_length=20, verbose_name="Подсветка клавиатуры", choices=KEYBOARD_BACKLIGHT_CHOICES, default=None, blank=True, null=True)
    touch_screen = models.CharField(max_length=20, verbose_name="Сенсорный экран", choices=TOUCH_SCREEN_CHOICES, blank=True, default=False)
    touch_screen_touches = models.IntegerField(verbose_name="Количество касаний одновременно", blank=True, null=True)
    screen_sizes = models.ManyToManyField(ScreenSize, verbose_name="Размер экрана", blank=True)
    screen_resolution = models.CharField(max_length=20, verbose_name="Разрешение экрана", choices=SCREEN_RESOLUTION_CHOICES, blank=True, null=True)
    power_supplies = models.ManyToManyField(PowerSupply, verbose_name="Блоки питания", blank=True)
    controllers  = models.ManyToManyField(Controller, verbose_name="Контроллеры", blank=True)
    sizes = models.ManyToManyField('Size', verbose_name="Размеры", blank=True)
    form_factor = models.CharField(max_length=20, verbose_name="Форм-фактор", choices=FORM_FACTOR_CHOICES, blank=True, null=True)


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


