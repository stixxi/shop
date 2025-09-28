from django.contrib import admin
from .models import CustomUser, AdApplication, Advertisement
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdApplication)
admin.site.register(Advertisement)