# Generated by Django 5.0.6 on 2024-06-11 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0065_alter_storage_size_alter_storage_size_tb_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='graphics',
            options={'ordering': ['size']},
        ),
        migrations.RemoveField(
            model_name='graphics',
            name='name',
        ),
        migrations.AddField(
            model_name='graphics',
            name='size',
            field=models.PositiveIntegerField(null=True, verbose_name='Объем видеокарты(ГБ)'),
        ),
        migrations.AddField(
            model_name='product',
            name='graphics',
            field=models.ManyToManyField(blank=True, to='QT_store.graphics', verbose_name='Видеокарта(дискретная)'),
        ),
    ]