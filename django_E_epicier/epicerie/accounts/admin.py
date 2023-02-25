from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Epicier,Client
# Register your models here.

admin.site.register(Client)
admin.site.register(Epicier)