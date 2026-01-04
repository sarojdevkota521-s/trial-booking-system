from django.contrib import admin
from .models import Catogery, Vehicle, Package, Booking, TrialTime
# Register your models here.
admin.site.register(Catogery)
admin.site.register(Vehicle)
admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(TrialTime)
