# Generated by Django 3.1.4 on 2020-12-17 14:14

from django.db import migrations, models
import electronic.models


class Migration(migrations.Migration):

    dependencies = [
        ('electronic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='device_type',
            field=models.CharField(choices=[(1, 'Mobile'), (2, 'Laptop')], default=electronic.models.DeviceType['Laptop'], max_length=255),
        ),
    ]
