# Generated by Django 3.0.2 on 2020-04-05 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realestate', '0002_auto_20200317_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(null=True)),
                ('pst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.post')),
                ('seenby', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
