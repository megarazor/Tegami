from django.db import models
from userController.models import Profile
import datetime

class PalList(models.Model):
    profile = models.ForeignKey(Profile, related_name="pal_list", null=True, on_delete=models.CASCADE)
    pal_list = models.ManyToManyField(Profile)

    @classmethod
    def make_pal(cls, current_profile, new_pal):
        p, created= cls.objects.get_or_create(profile=current_profile)
        p2, created= cls.objects.get_or_create(profile=new_pal)
        p.pal_list.add(new_pal)
        p2.pal_list.add(current_profile)
    
    @classmethod
    def remove_pal(cls, current_profile, old_pal):
        p, created= cls.objects.get_or_create(profile=current_profile)
        p2, created2= cls.objects.get_or_create(profile=old_pal)
        p.pal_list.remove(old_pal)
        p2.pal_list.remove(current_profile)
    
    @classmethod
    def is_pal(cls, current_profile, target_profile):
        p, created= cls.objects.get_or_create(profile=current_profile)
        if (created == True):
            return 0
        elif target_profile in p.pal_list.all():
            return 1
        return 0

class MatchRequest(models.Model):
    requester= models.ForeignKey(Profile, related_name="requester", null=True, on_delete=models.CASCADE)
    receiver= models.ForeignKey(Profile, related_name="receiver", null=True, on_delete=models.CASCADE)
    time= models.DateTimeField()

    @classmethod
    def create(cls, requester, receiver):
        request= cls(requester=requester, receiver=receiver, time=datetime.datetime.now())
        return request

