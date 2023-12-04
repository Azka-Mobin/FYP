from django.db import models
from client.models import Client

class Campaign(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

