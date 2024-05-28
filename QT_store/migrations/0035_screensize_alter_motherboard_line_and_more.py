# Generated by Django 5.0.6 on 2024-05-28 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0034_motherboard_line_alter_storage_size_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50, verbose_name='Размер экрана')),
            ],
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='line',
            field=models.CharField(choices=[('SOCKET', 'Socket'), ('FCBGA', 'FCBGA')], default='Socket', max_length=50, verbose_name='Линейка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='graphics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.graphics', verbose_name='Видеокарта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='operating_humidity',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Рабочая влажность'),
        ),
        migrations.AlterField(
            model_name='product',
            name='operating_system',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.operatingsystem', verbose_name='Операционная система'),
        ),
        migrations.AlterField(
            model_name='product',
            name='operating_temperature',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Температура эксплуатации'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ports',
            field=models.ManyToManyField(blank=True, to='QT_store.port', verbose_name='Порты и разъемы'),
        ),
        migrations.AlterField(
            model_name='product',
            name='processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.processor', verbose_name='Процессор'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ram',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.ram', verbose_name='Оперативная память'),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='QT_store.storage', verbose_name='Накопители'),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage_humidity',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Влажность хранения'),
        ),
        migrations.AlterField(
            model_name='product',
            name='storage_temperature',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Температура хранения'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Вес'),
        ),
    ]