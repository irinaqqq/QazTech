# Generated by Django 5.0.6 on 2024-06-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0047_alter_product_operating_system_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ram',
            name='size',
            field=models.CharField(max_length=10, null=True, verbose_name='Объем оперативной памяти(ГБ)'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='size',
            field=models.CharField(choices=[('120GB', '120 ГБ'), ('240GB', '240 ГБ'), ('480GB', '480 ГБ'), ('500GB', '500 ГБ'), ('1TB', '1 ТБ'), ('2TB', '2 ТБ'), ('4TB', '4 ТБ'), ('8TB', '8 ТБ'), ('16TB', '16 ТБ'), ('32TB', '32 ТБ'), ('64TB', '64 ТБ'), ('128TB', '128 ТБ'), ('256TB', '256 ТБ'), ('512TB', '512 ТБ'), ('1024TB', '1024 ТБ')], max_length=10, null=True, verbose_name='Объем накопителя'),
        ),
    ]
