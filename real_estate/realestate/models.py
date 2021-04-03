from django.db import models
# from django_mysql.models import ListCharField
from django.contrib.auth.models import User
# Create your models here.
class post(models.Model):
    P_TYPE = [
        ('House','House'),
        ('Plot', 'Plot'),
    ]

    S_TYPE = [
        ('Sale','Sale'),
        ('Rent', 'Rent'),
    ]


    status = models.CharField(max_length=4,choices=S_TYPE,)
    location = models.CharField(max_length=100)
    property_type = models.CharField(max_length=5,choices=P_TYPE,)
    area = models.FloatField()
    beds = models.PositiveIntegerField(default=None,null=True)
    baths = models.PositiveIntegerField(default=None,null=True)
    garage = models.PositiveIntegerField(default=None,null=True)
    price = models.FloatField()
    property_desc = models.TextField()

    author = models.ForeignKey(User,on_delete=models.CASCADE)



    def __str__(self):
        return "%s %s" % (self.author, self.id)

class media(models.Model):
    img = models.ImageField(upload_to='property_pics')
    pst = models.ForeignKey(post,on_delete=models.CASCADE)
    def __str__(self):
        return "%s %s" % (self.pst.id, self.id)


    
class reports(models.Model):
    views = models.IntegerField(null = True)
    pst = models.ForeignKey(post,on_delete=models.CASCADE)
    seenby = models.ManyToManyField(User)


class suggestions(models.Model):
    plots =  models.PositiveIntegerField(default=0,null=True)
    houses =  models.PositiveIntegerField(default=0,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)