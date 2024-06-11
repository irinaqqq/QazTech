# Generated by Django 5.0.6 on 2024-06-11 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0055_delete_controller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='controllers',
            field=models.ManyToManyField(blank=True, to='QT_store.controller', verbose_name='Контроллеры'),
        ),
    ]