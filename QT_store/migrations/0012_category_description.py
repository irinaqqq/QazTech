# Generated by Django 5.0.6 on 2024-05-23 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0011_alter_product_features'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=110, null=True, verbose_name='Описание(кратко)'),
        ),
    ]
