# Generated by Django 5.0.6 on 2024-05-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0003_graphics_operatingsystem_port_processor_ram_storage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
    ]
