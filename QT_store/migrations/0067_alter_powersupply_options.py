# Generated by Django 5.0.6 on 2024-06-11 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0066_alter_graphics_options_remove_graphics_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='powersupply',
            options={'ordering': ['power']},
        ),
    ]