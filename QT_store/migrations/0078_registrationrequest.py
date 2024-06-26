# Generated by Django 5.0.6 on 2024-06-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QT_store', '0077_alter_productdescription_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
            ],
        ),
    ]
