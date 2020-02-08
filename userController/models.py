from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Notifications(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    time= models.DateTimeField()
    content= models.TextField(max_length=200)
    read= models.BooleanField()
    url= models.URLField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    GENDER_FEMALE = 0
    GENDER_MALE = 1
    GENDER_CHOICES = [(GENDER_FEMALE, 'Female'), (GENDER_MALE, 'Male')]
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_MALE)

    intro = models.TextField(max_length=500, blank=True)
    
    COUNTRY_CHOICES = [
        ('VN', 'Vietnam'),
        ('JP', 'Japan')
        ]
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='JP')

    address = models.CharField(max_length=100, blank=True)
    DoB = models.DateField(null=True, blank=True)
    profile_pic = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
    
    def count_unread_notis(self):
        notis= self.user.notifications.filter(read=False).count()
        return notis

class Language(models.Model):
    lang_code = models.IntegerField(default=0)
    speaker = models.ForeignKey(User, related_name="language", on_delete=models.CASCADE, default=0)

