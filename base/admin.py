from django.contrib import admin
from .models import Catogery, Vehicle, Package, Booking, TrialTime,Timeslot, ContactMessage,Trainer

# Register your models here.
admin.site.register(Catogery)
admin.site.register(Vehicle)
admin.site.register(Package)
admin.site.register(ContactMessage)
admin.site.register(Booking)
admin.site.register(TrialTime)
admin.site.register(Timeslot)
admin.site.register(Trainer)
