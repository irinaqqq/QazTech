# Generated by Django 5.0.6 on 2024-06-26 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0081_alter_registrationrequest_initial_password_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
