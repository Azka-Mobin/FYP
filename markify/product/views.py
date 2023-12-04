import json 
import stripe
from concurrent.futures import ThreadPoolExecutor
from django.contrib.auth.decorators import login_required
from .models import Product, Advertisement
from .forms import AddProductForm, AddToCampaignForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .ai_models.ad_generator import get_ad_body, get_ad_title


@login_required
def products_list(request):
    products = Product.objects.filter(team=request.user.userprofile.active_team)
    return render(request, 'product/product_list.html', {
        'products': products,
    })

def products_list_all(request):
    products = Product.objects.all()
    return render(request, 'product/product_list_all.html', {
        'products': products,
    })
    
@login_required
def product_add(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.team = request.user.userprofile.active_team
            product.save()
            
            
            messages.success(request, "The product was created.")
                    
            return redirect('products:list')
    else:    
        form = AddProductForm()
    return render(request, 'product/product_add.html',{
        'form': form,
        'team':request.user.userprofile.active_team,        
    })   


def products_detail(request,pk):
    product = get_object_or_404(Product, pk=pk)
    is_owner = False
    try:
        if product.team == request.user.userprofile.active_team:
            is_owner = True
    except AttributeError:
        pass     
    return   render(request, 'product/product_detail.html', {
         'product':product,
         'is_owner':is_owner,
         })    
    
    
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, team=request.user.userprofile.active_team, pk=pk)    
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, "The changes were saved.")
                    
            return redirect('products:list')
    else:    
        form = AddProductForm(instance=product)        
    
    return render(request, 'product/product_edit.html',{
        'form': form,
    })    
    
    
@login_required
def product_delete(request, pk):
        product = get_object_or_404(Product, team = request.user.userprofile.active_team, pk=pk)
        product.delete()
        
        messages.success(request, "The product was deleted.")
        return redirect('products:list')
    
def product_buy(request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        if request.method == 'POST':
            pass

@login_required
def generate_ad(request, pk):
        product = get_object_or_404(Product, team = request.user.userprofile.active_team, pk=pk)
        
        with ThreadPoolExecutor() as executor:
            ad_description = executor.submit(get_ad_body,product_name= product.name, product_description=product.description, product_price=product.price)
            ad_title = executor.submit(get_ad_title,product_name= product.name, product_description=product.description)
            ad_title = ad_title.result()
            ad_description = ad_description.result()

        if ad_title == "":
            ad_title = "Check This Out: "+product.name
        elif ad_title == "Please provide the ad title.":
            ad_title = "Check This Out: "+product.name    
        elif ad_title.split()[0] == 'Answer:':
            title =ad_title
            ad_title = ' '.join(title.split()[1:]) 
        elif ad_title == "Please provide the ad title for the given product description.":
            ad_title = "Check This Out: "+product.name
        elif len(ad_title) < 5:
            ad_title = "Check This Out: "+product.name     
            
        Advertisement.objects.create(
            product=product,
            title=ad_title, 
            description=ad_description
            )        
        messages.success(request, "The Ad was created succesfully.")        
        return redirect('products:list')


def ad_list(request):    
    ads = Advertisement.objects.all()
    return render(request, 'ad/ad_list.html', {
        'ads': ads,
    })

def ad_detail(request,pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    is_owner = False
    try:
        if ad.product.team == request.user.userprofile.active_team:
            is_owner = True
        else:
            ad.activity += 1  
            ad.save()  
    except AttributeError:
        ad.activity += 1
        ad.save()
         
    return   render(request, 'ad/ad_detail.html', {
         'ad':ad,
         'description':ad.description,
         'is_owner':is_owner,
         })    
    
@login_required
def ad_delete(request, pk):
        ad = get_object_or_404(Advertisement, pk=pk)
        ad.delete()
        
        messages.success(request, "The Ad was deleted.")
        return redirect('ads:list')    
    
    

@login_required
def ad_add_campaign(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        form = AddToCampaignForm(request.POST)
        if form.is_valid():
            selected_campaign = form.cleaned_data['campaign']
            ad.campaign = selected_campaign  # Associate the selected campaign with the ad
            ad.save()
            messages.success(request, "The ad was added to the campaign.")
            return redirect('ads:list')
    else:
        form = AddToCampaignForm()

    return render(request, 'ad/add_campaign.html', {
        'form': form,
        'ad': ad,
    })




