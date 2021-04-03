from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE = [
        ('SL','Seller'),
        ('BY', 'Buyer'),
    ]
    Type = models.CharField(
    max_length=2,
    choices=TYPE,
    )
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    country=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    zip_code=models.CharField(max_length=10,null=True)
    phone=models.CharField(max_length=20,null=True)
#    form_completed=models.BooleanField(default=False) # this field checks if form is completed or not 

    def __str__(self):
        return "%s %s" % (self.user, self.Type)