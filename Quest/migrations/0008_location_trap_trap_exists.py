# Generated by Django 5.1.1 on 2024-10-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quest', '0007_location_is_it_tech'),
    ]

    operations = [
        migrations.AddField(
            model_name='location_trap',
            name='trap_exists',
            field=models.BooleanField(default=True),
        ),
    ]
