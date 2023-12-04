from .models import Campaign
from django.utils import timezone

def campaign_expired(request):
    
    campaigns = Campaign.objects.all()
    for campaign in campaigns:
        if campaign.end_date < timezone.now().date():
            campaign.active = False
            campaign.save()
    
    return {'campaigns': campaigns}        
    