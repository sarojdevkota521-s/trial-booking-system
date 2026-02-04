from datetime import timedelta
from django.utils import timezone

from django.db import models
from django.utils.timezone import now
from django.db.models import Q, UniqueConstraint
from django.contrib.auth.models import User
# Create your models here.
class Catogery(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

  
class Vehicle(models.Model):
    
    catogery = models.ForeignKey(Catogery, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    photo=models.ImageField(upload_to='vehicle_photos/', null=True, blank=True)


    def __str__(self):
        return f"{self.name} - {self.catogery.name}"
    
class Package(models.Model):
    vehicle=models.ForeignKey(Catogery, on_delete=models.CASCADE)
    package_name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    time=models.CharField(max_length=100)
    duration_days=models.IntegerField()

    def __str__(self):
        return f" {self.package_name} - {self.vehicle.name} - {self.price} "
    
class Timeslot(models.Model):
    time=models.CharField(max_length=100)

    def __str__(self):
        return self.time
    
class TrialTime(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    time = models.ForeignKey(Timeslot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle.name} - {self.time}"

    class Meta:
        ordering = ['time']
        unique_together = ('vehicle', 'time')


class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    package=models.ForeignKey(Package, on_delete=models.CASCADE)
    trial_time=models.ForeignKey(TrialTime, on_delete=models.CASCADE,  related_name='bookings')
    customer_name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    message=models.TextField()
    payment_status=models.BooleanField(default=False)
    payment_uuid = models.CharField(max_length=100, blank=True, null=True)
    booking_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)
    is_active=models.BooleanField(default=False)

    

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # first save to get booking_date
        super().save(*args, **kwargs)

        # set expiry date on creation
        if is_new and not self.expiry_date:
            self.expiry_date = self.booking_date + timedelta(
                days=self.package.duration_days
            )
            super().save(update_fields=['expiry_date'])

        # deactivate if expired
        if self.expiry_date and self.expiry_date < timezone.now().date():
            if self.is_active:
                self.is_active = False
                super().save(update_fields=['is_active'])


    def __str__(self):
        return f"Booking for {self.vehicle.name} by {self.customer_name}"

    

    class Meta:
        constraints = [
          UniqueConstraint(
            fields=['vehicle', 'trial_time'],
            condition=Q(is_active=True),
            name='unique_active_booking'
        )
    ]
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='trainer_photos/', null=True, blank=True)
    specialization = models.CharField(max_length=200)
    experience_years = models.IntegerField()
    bio = models.TextField()

    def __str__(self):
        return self.name