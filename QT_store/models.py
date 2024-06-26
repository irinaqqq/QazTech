from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=110, verbose_name="Описание(кратко)", null=True)
    image = models.ImageField(upload_to='category_images/', verbose_name="Фото", null=True)
    imageback = models.ImageField(upload_to='category_images/', verbose_name="Задний фон", null=True)
    # Другие поля, если нужно
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

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
        if self.series:
            self.name = f"{self.brand.name} {self.line.name} {self.series}"
        else:
            self.name = f"{self.brand.name} {self.line.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class OperatingSystem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Операционная система")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Graphics(models.Model):
    size = models.PositiveIntegerField(verbose_name="Объем видеокарты(ГБ)", null=True)

    def __str__(self):
        return f"{self.size} ГБ"
    
    class Meta:
        ordering = ['size']
    
class RAM(models.Model):
    TYPE_CHOICES = [
        ('DDR3', 'DDR3'),
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5'),
    ]

    size = models.PositiveIntegerField(verbose_name="Объем оперативной памяти(ГБ)", null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип оперативной памяти", null=True)

    class Meta:
        ordering = ['-type', models.F('size').asc(nulls_last=True)]

    def __str__(self):
        return f"{self.size} ({self.type})"

from django.db import models
from django.core.exceptions import ValidationError

class Storage(models.Model):
    HDD = 'HDD'
    SSD = 'SSD'
    NVME = 'NVMe'
    
    STORAGE_TYPE_CHOICES = [
        (HDD, 'HDD'),
        (SSD, 'SSD'),
        (NVME, 'NVMe'),
    ]

    size = models.PositiveIntegerField(verbose_name="Объем накопителя(ГБ)", null=True, blank=True)
    size_tb = models.FloatField(verbose_name="Объем накопителя(ТБ)", null=True, blank=True)
    type = models.CharField(max_length=4, choices=STORAGE_TYPE_CHOICES, default=SSD, verbose_name="Тип накопителя", null=True)

    class Meta:
        unique_together = ('size', 'type')
        ordering = ['-type', models.F('size').asc(nulls_last=True)]

    def clean(self):
        if not self.size and not self.size_tb:
            raise ValidationError('Either size (ГБ) or size_tb (ТБ) must be provided.')
        
        if self.size_tb and not self.size:
            self.size = int(self.size_tb * 1024)
        elif self.size and not self.size_tb:
            self.size_tb = self.size / 1024

    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean() is called on save
        super().save(*args, **kwargs)

    def __str__(self):
        if self.size:
            if self.size < 1024:
                return f"{self.size} ГБ ({self.get_type_display()})"
            else:
                tb_size = self.size / 1024
                return f"{tb_size:.1f} ТБ ({self.get_type_display()})"
        elif self.size_tb:
            return f"{self.size_tb:.1f} ТБ ({self.get_type_display()})"
        else:
            return f"({self.get_type_display()})"


class Motherboard(models.Model):
    
    TYPE_CHOICES = [
        ('Socket', 'Socket'),
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
    class Meta:
        ordering = ['name']

class Port(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название порта", unique=True)

    def __str__(self):
        return self.name

class ScreenSize(models.Model):
    size = models.CharField(max_length=50, verbose_name="Размер экрана", unique=True)

    def __str__(self):
        return self.size

class PowerSupply(models.Model):
    power = models.PositiveIntegerField(verbose_name="Мощность", unique=True)


    def __str__(self):
        return f"{self.power} W"
    
    class Meta:
        ordering = ['power']

class Controller(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.name
    
class KeyboardLight(models.Model):
    light = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.light
    
class ScreenResolution(models.Model):
    resolution = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.resolution
    
class FormFactor(models.Model):
    formf = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.formf
    
class KeyboardSet(models.Model):
    set = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.set
    
class TouchST(models.Model):
    touches = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.touches
    
class ScreenType(models.Model):
    stype = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.stype
    
class WebCam(models.Model):
    cam = models.CharField(max_length=50, verbose_name="Название", unique=True)

    def __str__(self):
        return self.cam

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=100, verbose_name="Название", unique=True)
    features = models.CharField(max_length=60, verbose_name="Особенности(кратко)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    processor = models.ManyToManyField(Processor, verbose_name="Процессор", blank=True)
    mother = models.ManyToManyField(Motherboard, verbose_name="Материнская плата", blank=True)
    ram = models.ManyToManyField(RAM, verbose_name="Оперативная память", blank=True)
    storage = models.ManyToManyField(Storage, verbose_name="Накопители", blank=True)
    graphics = models.ManyToManyField(Graphics, verbose_name="Видеокарта(дискретная)", blank=True)
    operating_system = models.ManyToManyField(OperatingSystem, verbose_name="Операционная система", blank=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Вес", null=True, blank=True)
    screen_sizes = models.ManyToManyField(ScreenSize, verbose_name="Размер экрана", blank=True)
    screen_type = models.ManyToManyField(ScreenType, verbose_name="Тип экрана", blank=True)
    screen_resolution = models.ManyToManyField(ScreenResolution, verbose_name="Разрешение экрана", blank=True)
    touch_screen_touches = models.ManyToManyField(TouchST, verbose_name="Количество касаний одновременно", blank=True)
    formfactor = models.ManyToManyField(FormFactor, verbose_name="Форм-фактор", blank=True)
    webcam = models.ManyToManyField(WebCam, verbose_name="Веб камера", blank=True)
    keyset = models.ManyToManyField(KeyboardSet, verbose_name="Комплект клавиатура и мышь", blank=True)
    keyboard_backlight = models.ManyToManyField(KeyboardLight, verbose_name="Подсветка клавиатуры", blank=True)
    power_supplies = models.ManyToManyField(PowerSupply, verbose_name="Блоки питания", blank=True)
    operating_temperature = models.CharField(max_length=20, verbose_name="Температура эксплуатации", null=True, blank=True)
    storage_temperature = models.CharField(max_length=20, verbose_name="Температура хранения", null=True, blank=True)
    operating_humidity = models.CharField(max_length=20, verbose_name="Рабочая влажность", null=True, blank=True)
    storage_humidity = models.CharField(max_length=20, verbose_name="Влажность хранения", null=True, blank=True)
    sizes = models.ManyToManyField('Size', verbose_name="Размеры", blank=True)
    controllers  = models.ManyToManyField(Controller, verbose_name="Контроллеры", blank=True)
    # ports = models.ManyToManyField(Port, verbose_name="Порты и разъемы", blank=True)
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.pk)])
    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
    # Удаляем связанные изображения из папки
        for image in self.images.all():
            image_path = os.path.join(settings.MEDIA_ROOT, image.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        # Затем вызываем оригинальный метод delete
        super(Product, self).delete(*args, **kwargs)
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Продукт")
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение", null=True, blank=True)

    def __str__(self):
        return f"Изображение для {self.product.name}"


@receiver(post_delete, sender=ProductImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
        if os.path.exists(image_path):
            os.remove(image_path)

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, related_name='descriptions', on_delete=models.CASCADE, verbose_name="Продукт")
    title = models.CharField(max_length=255, verbose_name="Заголовок", null=True, blank=True)
    image = models.ImageField(upload_to='product_descriptions/', verbose_name="Фото", blank=True, null=True)
    text = models.TextField(verbose_name="Описание", null=True, blank=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.message[:20]}'
    
class RegistrationRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
class Custom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    initial_password = models.CharField(max_length=100, blank=True, null=True, editable=False)

    def __str__(self):
        return f"{self.user.username}'s profile"