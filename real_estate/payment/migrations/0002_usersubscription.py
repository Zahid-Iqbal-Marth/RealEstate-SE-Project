# Generated by Django 3.0.2 on 2020-03-20 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_count', models.IntegerField(default=0)),
                ('post_count', models.IntegerField(default=0)),
                ('sub_date', models.DateField(null=True)),
                ('stripe_cust_id', models.CharField(max_length=200)),
                ('sub_status', models.CharField(max_length=100)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.package')),
            ],
        ),
    ]