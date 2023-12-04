from django.db import models
from django.contrib.auth.models import User
from team.models import Team

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile", on_delete=models.CASCADE)
    active_team =models.ForeignKey(Team, related_name="userprofiles", on_delete=models.CASCADE, blank=True, null=True)
    
