# Generated by Django 5.0.6 on 2024-05-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0013_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='processor',
            name='brand',
            field=models.CharField(max_length=50, null=True, verbose_name='Бренд'),
        ),
        migrations.AddField(
            model_name='processor',
            name='line',
            field=models.CharField(max_length=50, null=True, verbose_name='Линейка'),
        ),
        migrations.AddField(
            model_name='processor',
            name='series',
            field=models.CharField(max_length=50, null=True, verbose_name='Серия'),
        ),
        migrations.AlterField(
            model_name='processor',
            name='name',
            field=models.CharField(editable=False, max_length=255, verbose_name='Процессор'),
        ),
    ]
