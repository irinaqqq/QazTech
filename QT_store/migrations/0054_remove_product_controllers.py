# Generated by Django 5.0.6 on 2024-06-11 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0053_touchst_remove_product_discrete_graphics_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='controllers',
        ),
    ]
