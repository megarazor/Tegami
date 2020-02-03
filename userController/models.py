from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intro = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=100, blank=True)
    DoB = models.DateField(null=True, blank=True)
    profile_pic = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

class Language(models.Model):
    lang_code = models.IntegerField(default=0)
    speaker = models.ForeignKey(User, related_name="language", on_delete=models.CASCADE, default=0)

    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()