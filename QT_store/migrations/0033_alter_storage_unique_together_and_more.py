# Generated by Django 5.0.6 on 2024-05-24 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0032_storage_size_custom_alter_ram_size_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='storage',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='storage',
            name='size_custom',
        ),
    ]