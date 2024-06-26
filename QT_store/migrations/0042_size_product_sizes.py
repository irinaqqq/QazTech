# Generated by Django 5.0.6 on 2024-05-28 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0041_controller_product_controllers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, to='QT_store.size', verbose_name='Размеры'),
        ),
    ]
