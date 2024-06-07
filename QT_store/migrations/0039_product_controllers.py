# Generated by Django 5.0.6 on 2024-05-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0038_powersupply_alter_product_screen_resolution_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='controllers',
            field=models.CharField(blank=True, choices=[(None, 'Нет'), ('RAID', 'RAID-адаптер'), ('HBA', 'HBA-адаптер')], default=None, max_length=50, verbose_name='Контроллеры'),
        ),
    ]
