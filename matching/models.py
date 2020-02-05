from django.db import models
from userController.models import Profile

class PalList(models.Model):
    profile = models.ForeignKey(Profile, related_name="owner", null=True, on_delete=models.CASCADE)
    pal_list = models.ManyToManyField(Profile)
    
    @classmethod
    def make_pal(cls, current_user, new_pal):
        pal= cls.objects.get_or_create(
            profile = current_user
        )
        pal.pal_list.add(new_pal)

    @classmethod
    def remove_pal(cls, current_user, to_be_removed_pal):
        pal= cls.objects.get_or_create(
            user = current_user
        )
        pal.pal_list.remove(to_be_removed_pal)

    def __str__(self):
        return str(self.user)

