# Generated by Django 5.0.6 on 2024-07-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0083_remove_registrationrequest_initial_password_custom'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationrequest',
            name='organisation',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
