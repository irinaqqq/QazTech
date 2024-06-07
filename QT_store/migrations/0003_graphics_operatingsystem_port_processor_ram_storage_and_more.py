# Generated by Django 5.0.6 on 2024-05-20 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0002_remove_product_specifications_product_graphics_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graphics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Видеокарта')),
            ],
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Операционная система')),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название порта')),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Процессор')),
            ],
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=255, verbose_name='Объем оперативной памяти')),
                ('type', models.CharField(max_length=255, verbose_name='Тип оперативной памяти')),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=255, verbose_name='Объем накопителя')),
                ('type', models.CharField(choices=[('HDD', 'Hard Disk Drive (HDD)'), ('SSD', 'Solid-State Drive (SSD)'), ('NVMe', 'Non-Volatile Memory Express (NVMe)')], default='SSD', max_length=4, verbose_name='Тип накопителя')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='ports',
        ),
        migrations.AlterField(
            model_name='product',
            name='graphics',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.graphics', verbose_name='Видеокарта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='operating_system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.operatingsystem', verbose_name='Операционная система'),
        ),
        migrations.AlterField(
            model_name='product',
            name='processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.processor', verbose_name='Процессор'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ram',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.ram', verbose_name='Оперативная память'),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.storage', verbose_name='Накопители'),
        ),
        migrations.AddField(
            model_name='product',
            name='ports',
            field=models.ManyToManyField(to='QT_store.port', verbose_name='Порты и разъемы'),
        ),
    ]
