# Generated by Django 5.0.6 on 2024-06-25 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0079_registrationrequest_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrationrequest',
            old_name='password',
            new_name='initial_password',
        ),
    ]