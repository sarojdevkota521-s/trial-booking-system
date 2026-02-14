from django.contrib import admin
from .models import PasswordReset
# Register your models here.
admin.site.site_header="Trial Center Admin"
admin.site.register(PasswordReset)

