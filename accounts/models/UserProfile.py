from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models.User import User


class UserProfile(models.Model):
    class Genders(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="profile")
    
    gender = models.CharField(_("Gender"), max_length=1, choices=Genders.choices, default=Genders.MALE)
    phone_1 = models.CharField(_("Phone (Main)"), max_length=20)
    phone_2 = models.CharField(_("Phone (Other)"), max_length=20, null=True, blank=True)
    
    