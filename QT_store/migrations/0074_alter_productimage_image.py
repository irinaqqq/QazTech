# Generated by Django 5.0.6 on 2024-06-14 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0073_category_imageback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(default='product_images/placeholder.png', upload_to='product_images/', verbose_name='Изображение'),
        ),
    ]
