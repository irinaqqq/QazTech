# Generated by Django 5.0.6 on 2024-06-11 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0062_alter_storage_options_alter_storage_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storage',
            options={'ordering': ['-type', models.OrderBy(models.F('size'), nulls_last=True)]},
        ),
        migrations.AddField(
            model_name='storage',
            name='size_tb',
            field=models.FloatField(null=True, verbose_name='Объем накопителя(ТБ)'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='type',
            field=models.CharField(choices=[('HDD', 'HDD'), ('SSD', 'SSD')], default='SSD', max_length=4, null=True, verbose_name='Тип накопителя'),
        ),
    ]
