from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import User


# Create your models here.
class PasswordReset(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_when=models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"password reset for {self.user.username} at {self.created_when }"

# class Profile(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,null =True, blank =True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     bio= models.TextField(blank=True, null=True)
    
#     profile_image = models.ImageField(upload_to='photo', blank=True,null=True, default="avatar.svg")

#     def __str__(self):
#         return self.user.username