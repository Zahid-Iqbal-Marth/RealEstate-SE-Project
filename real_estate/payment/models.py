from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
# Create your models here.


class package(models.Model):
    Pack_TYPE = [
        ('Free','Free'),
        ('One-Month', 'One Month'),
        ('Six-Months', 'Six Months'),
    ]
    package_type = models.CharField(max_length = 10,choices = Pack_TYPE,)
    price = models.IntegerField(default = 0)
    ad_posting_limit = models.IntegerField(default = 0)

    def __str__(self):
        return "%s %s" % (self.package_type, self.price)


class UserSubscription(models.Model):
    pack=models.ForeignKey(package,on_delete=models.CASCADE,null=True)
    paid_count=models.IntegerField(default=0)
    post_count=models.IntegerField(default=0)
    sub_date=models.DateField(null=True)
    stripe_cust_id=models.CharField(max_length=200)
    name=models.ForeignKey(User,on_delete=models.CASCADE)

    s_status = [
        ('N','None'),
        ('S', 'Subscribed'),
        ('E', 'Expired'),
    ]

    sub_status=models.CharField(max_length = 1,choices = s_status,default='N')# UserSubscription status



    def __str__(self):
        return "%s %s" % (self.name, self.pack)