# Generated by Django 5.0.6 on 2024-07-02 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0086_registrationrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom',
            name='organization',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='custom',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='registrationrequest',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
