from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import Campaign
from .forms import AddClientForm
from client.models import Client
from product.models import Advertisement
import json



def campaigns_list(request):
    campaigns = Campaign.objects.filter(active=True)
    return render(request, 'campaigns/campaign_list.html', {'campaigns': campaigns})


def campaigns_client(request,pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    campaign = ad.campaign
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            if campaign is None:
                messages.success(request, 'This ad is not part of a campaign yet. Please try later.')
                return redirect('/')
            selected_name = form.cleaned_data['name']
            selected_email = form.cleaned_data['email']
            
            client = Client.objects.filter(email=selected_email)
            if client.exists():
                client = client[0]
            else:
                client = Client.objects.create(name=selected_name, email=selected_email)
                client.save()
           
            mappings = json.load(open('misc/mappings.json' ,'r')) 
            client_email = mappings.get(campaign.title, None)
            
            if client_email is None:
                mappings[campaign.title] = [client.email]
            else:
                mappings[campaign.title].append(client.email)   
            
            json.dump(mappings, open('misc/mappings.json' ,'w'))     
                    
            
            messages.success(request, "You will be notified about upcoming products")
            return redirect('ads:list')
    else:
        form = AddClientForm()

    return render(request, 'campaigns/campaign_add_clients.html', {
        'form': form,
        'ad' : ad,
    })

def send_email(request, pk):
    campaign = Campaign.objects.filter(active=True).get(pk=pk)
    if campaign is None:
        return HttpResponse('Invalid campaign')
    mappings = json.load(open('misc/mappings.json' ,'r')) 
    clients = mappings.get(campaign.title, None)
    if clients is None:
        messages.success(request, 'No client registered for this campaign')
        return redirect('campaigns:list')
    ads = Advertisement.objects.filter(campaign=campaign).order_by('-activity')
    if len(ads) == 0:
        messages.success(request, 'No advertisement found for this campaign')
        return redirect('campaigns:list')
    
    subject = "From Markify: " + campaign.title
    
    
    from_email = settings.EMAIL_HOST_USER
    
    client_emails = clients

    try:
        for ad in ads:    
            message = ad.description + "\nFor more information visit our website"
            send_mail(subject, message, from_email, client_emails,)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')    
    messages.success(request, 'The client has recieved your campaign emails.')
    return redirect('campaigns:list')

