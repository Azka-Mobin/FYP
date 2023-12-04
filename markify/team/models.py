from django.db import models
from django.contrib.auth.models import User
class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True , null=True)
    max_leads = models.IntegerField()    
    max_clients = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    plan = models.ForeignKey(Plan, related_name='teams', blank=True, null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    
    
class Request(models.Model):
    user = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  self.user.username
    