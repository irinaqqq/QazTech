# Generated by Django 5.0.6 on 2024-06-06 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0048_alter_ram_size_alter_storage_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='size',
            field=models.CharField(max_length=10, null=True, verbose_name='Объем накопителя(ГБ)'),
        ),
    ]