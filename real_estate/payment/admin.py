from django.contrib import admin

# Register your models here.
from .models import package, UserSubscription

admin.site.register(package)
admin.site.register(UserSubscription)