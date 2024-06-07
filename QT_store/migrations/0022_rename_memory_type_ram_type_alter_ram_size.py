# Generated by Django 5.0.6 on 2024-05-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0021_ramtype_rename_brand_procbrand_rename_line_procline_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ram',
            old_name='memory_type',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='ram',
            name='size',
            field=models.CharField(choices=[('4GB', '4 ГБ'), ('8GB', '8 ГБ'), ('16GB', '16 ГБ'), ('32GB', '32 ГБ'), ('64GB', '64 ГБ'), ('128GB', '128 ГБ')], max_length=5, verbose_name='Объем оперативной памяти'),
        ),
    ]
