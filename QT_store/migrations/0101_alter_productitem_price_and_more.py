# Generated by Django 5.0.6 on 2024-07-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0100_alter_productitem_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]
