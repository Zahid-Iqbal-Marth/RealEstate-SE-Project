# Generated by Django 3.0.2 on 2020-04-11 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0003_reports'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='property_type',
            field=models.CharField(choices=[('House', 'House'), ('Plot', 'Plot')], max_length=5),
        ),
    ]
