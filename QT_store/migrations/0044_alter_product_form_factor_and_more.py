# Generated by Django 5.0.6 on 2024-05-28 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0043_product_form_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='form_factor',
            field=models.CharField(blank=True, choices=[(None, 'Нет'), ('Horizontal', 'Горизонтальный'), ('Vertical', 'Вертикальный')], max_length=20, null=True, verbose_name='Форм-фактор'),
        ),
        migrations.AlterField(
            model_name='product',
            name='keyboard_backlight',
            field=models.CharField(blank=True, choices=[(None, 'Нет'), (False, 'Без подсветки'), (True, 'С подсветкой')], default=None, max_length=20, null=True, verbose_name='Подсветка клавиатуры'),
        ),
        migrations.AlterField(
            model_name='product',
            name='touch_screen',
            field=models.CharField(choices=[(True, 'Да'), (False, 'Нет')], default=False, max_length=20, verbose_name='Сенсорный экран'),
        ),
        migrations.AlterField(
            model_name='product',
            name='webcam',
            field=models.CharField(blank=True, choices=[(None, 'Нет'), (False, 'Без встроенной вебкамеры'), (True, 'Со встроенной веб камерой')], default=None, max_length=20, verbose_name='Веб камера'),
        ),
    ]
