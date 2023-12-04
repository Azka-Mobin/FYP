from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from .forms import AddCommentForm
from .models import Lead
from client.models import Client, Comment as ClientComment
from team.models import Team


class LeadListView(ListView):
    model = Lead
    
    def get_queryset(self):
        query_set = super(LeadListView,self).get_queryset()
        return query_set.filter(created_by=self.request.user, converted_to_client=False)

    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class LeadDetailView(DetailView):
    model = Lead
    
    def get_queryset(self):
        query_set = super(LeadDetailView,self).get_queryset()
        return query_set.filter(created_by=self.request.user, converted_to_client=False, pk=self.kwargs.get('pk'))
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        
        return context


class LeadDeleteView(DeleteView, SuccessMessageMixin):
    model = Lead

    success_url = reverse_lazy('leads:list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs) 
    
    def get_queryset(self):
        query_set = super(LeadDeleteView,self).get_queryset()
        return query_set.filter(created_by=self.request.user, converted_to_client=False, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    success_message = "The lead was deleted successfully."

class LeadCreateView(CreateView, SuccessMessageMixin):
    model=Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)    
    success_url = reverse_lazy('leads:list')
    success_message = "The lead was created successfully"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def form_valid(self, form):
        
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.active_team
        self.object.save()
        
        return redirect(self.get_success_url())     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = self.request.user.userprofile.active_team
        context["title"] = "Add Lead"
        
        return context
    

        
class LeadUpdateView(UpdateView, SuccessMessageMixin):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')
    success_message = "The lead was updated successfully"
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs) 
    
    def get_queryset(self):
        query_set = super(LeadUpdateView,self).get_queryset()
        return query_set.filter(created_by=self.request.user, converted_to_client=False, pk=self.kwargs.get('pk'))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Lead"
        
        return context


class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
            
            return redirect('leads:detail', pk=pk)
            
            
class ConvertToClientView(View):
    success_url = reverse_lazy('leads:list')
    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, created_by= request.user, pk=self.kwargs.get('pk'))
        
        client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description,
        team = request.user.userprofile.active_team,
        created_by=request.user,
        )
        lead.converted_to_client = True
        lead.save() 
        
        #Convert lead comments to client comments
        comments = lead.comments.all()
        
        for comment in comments:
            newcomment = ClientComment.objects.create(
                client=client,
                content = comment.content,
                created_by = comment.created_by, 
                team = request.user.userprofile.active_team,
            )
        
        messages.success(request, "The lead was converted to client.")
        return redirect('leads:list')       
        

        