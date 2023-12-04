from django import forms

from .models import Product, Advertisement
from campaigns.models import Campaign

class AddProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('name', 'price', 'description',)

class AddToCampaignForm(forms.Form):
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.filter(active=True),
        label="Select an Active Campaign",
        empty_label=None
    )
        