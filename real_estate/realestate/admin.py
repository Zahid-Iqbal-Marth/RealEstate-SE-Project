from django.contrib import admin

# Register your models here.
from .models import post, media, reports, suggestions
# Register your models here.


admin.site.register(post)
admin.site.register(media)
admin.site.register(reports)

admin.site.register(suggestions)

