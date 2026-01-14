from django.core.management.base import BaseCommand
from django.utils import timezone
from base.models import Booking

class Command(BaseCommand):
    help = "Deactivate expired bookings"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        updated = Booking.objects.filter(
            is_active=True,
            expiry_date__lt=today
        ).update(is_active=False)

        self.stdout.write(f"{updated} bookings deactivated")
