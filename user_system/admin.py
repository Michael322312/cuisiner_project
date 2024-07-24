from django.contrib import admin
from user_system.models import CustomUser, UserPreference
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserPreference)