from django.db import models
from django.contrib.auth.models import User
from .utils import resize_image, convert_type_image


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    simbrief_pilot_id = models.CharField(max_length=20, blank=True, default="")
    picture_profile = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        if self.picture_profile:
            resized_image = resize_image(self.picture_profile)
            converted_image = convert_type_image(
                resized_image,
                self.user.username
            )
            self.picture_profile = converted_image
        return super().save(*args, **kwargs)
