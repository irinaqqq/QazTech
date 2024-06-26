# Generated by Django 5.0.6 on 2024-05-24 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0020_remove_processor_unique_processor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RAMType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тип оперативной памяти')),
            ],
        ),
        migrations.RenameModel(
            old_name='Brand',
            new_name='ProcBrand',
        ),
        migrations.RenameModel(
            old_name='Line',
            new_name='ProcLine',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='type',
        ),
        migrations.AddField(
            model_name='ram',
            name='memory_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='QT_store.ramtype', verbose_name='Тип оперативной памяти'),
        ),
    ]
