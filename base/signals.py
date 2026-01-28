# # booking/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.admin.models import LogEntry, ADDITION
# from django.contrib.contenttypes.models import ContentType
# from django.utils.timezone import now
# from .models import Booking

# @receiver(post_save, sender=Booking)
# def booking_admin_notification(sender, instance, created, **kwargs):
#     if created:
#         LogEntry.objects.create(
#             user_id=1,  # 🔴 must be a valid admin user ID
#             content_type=ContentType.objects.get_for_model(instance),
#             object_id=str(instance.pk),
#             object_repr=str(instance),
#             action_flag=ADDITION,
#             change_message="New booking created",
#             action_time=now()
#         )
