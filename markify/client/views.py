from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import AddClientForm, AddCommentForm

@login_required
def clients_list(request):
    clients = Client.objects.all()
    
    
    return render(request, 'client/client_list.html', {
        'clients': clients,
    })

@login_required
def clients_detail(request,pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
         form = AddCommentForm(request.POST)
         
         if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            if request.user.is_authenticated:
                comment.created_by = request.user
            comment.client = client
            comment.save()
            
            return redirect('clients:detail', pk=pk)
    else:
        form = AddCommentForm()   
         
        return   render(request, 'client/client_detail.html', {
         'client':client,
         'form':form,
         })

@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            
            
            messages.success(request, "The client was created.")
                    
            return redirect('clients:list')
    else:    
        form = AddClientForm()
    return render(request, 'client/add_client.html',{
        'form': form,       
    })    


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)    
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "The changes were saved.")
                    
            return redirect('clients:list')
    else:    
        form = AddClientForm(instance=client)        
    
    return render(request, 'client/edit_client.html',{
        'form': form,
    })

@login_required
def clients_delete(request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        
        messages.success(request, "The client was deleted.")
        return redirect('clients:list')
    

    