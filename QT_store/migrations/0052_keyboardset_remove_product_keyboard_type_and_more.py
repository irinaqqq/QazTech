# Generated by Django 5.0.6 on 2024-06-11 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0051_formfactor_alter_category_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyboardSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='keyboard_type',
        ),
        migrations.AddField(
            model_name='product',
            name='keyset',
            field=models.ManyToManyField(blank=True, to='QT_store.keyboardset', verbose_name='Комплект клавиатура и мышь'),
        ),
    ]
