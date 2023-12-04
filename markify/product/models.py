from django.db import models
from team.models import Team
from userprofile.models import User
from campaigns.models import Campaign


class Product(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name='products', on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Advertisement(models.Model):
    product = models.ForeignKey(Product, related_name='advertisements', on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, related_name='advertisements', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    activity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)    

    def __str__(self):
        return self.title
