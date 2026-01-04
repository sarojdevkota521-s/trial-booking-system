from django.db import models

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
class TrialTime(models.Model):
    time=models.CharField(max_length=100)
    
    def __str__(self):
        return self.time
    class Meta:
        ordering = ['time']

class Booking(models.Model):
    vehicle=models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    package=models.ForeignKey(Package, on_delete=models.CASCADE)
    time=models.ForeignKey(TrialTime, on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    message=models.TextField()
    booking_date=models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"Booking for {self.vehicle.name} by {self.customer_name}"
    
    class Meta:
        ordering = ['-booking_date']



