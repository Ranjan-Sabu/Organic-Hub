from django.contrib import admin
from .models import Registration
from .models import UserProfile

# Register your models here.
admin.site.register(Registration)
admin.site.register(UserProfile)