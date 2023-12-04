from django.shortcuts import render, get_object_or_404, redirect
from .models import Team, Request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TeamForm


@login_required
def teams_list(request):
    teams = Team.objects.filter(members__in=[request.user])
    return render(request, 'team/teams_list.html', {
        'teams': teams
    })
    
@login_required
def teams_activate(request,pk):
    team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
    userprofile = request.user.userprofile
    userprofile.active_team= team  
    userprofile.save()
    
    return redirect('teams:detail',pk=pk)  
    

@login_required
def edit_team(request,pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated successfully')
            return redirect('userprofile:myaccount')
    else:    
        form = TeamForm(instance=team)
    
    return render(request, 'team/edit_team.html',{
        'team':team,
        'form':form
    })

@login_required
def list_teams_all(request):
    teams = Team.objects.all()
    return render(request, 'team/teams_list_all.html', {
        'teams': teams
    })


@login_required
def join_team(request,pk):
    team = get_object_or_404(Team, pk=pk) 
    Request.objects.create(user=request.user, team=team)
    messages.success(request, 'Request sent successfully')
    return redirect('teams:detail',pk=pk)

    
@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user
            team.save()
            team.members.add(request.user)
            team.save()
            messages.success(request, 'Team created successfully')
            return redirect('userprofile:myaccount')
    else:    
        form = TeamForm()
    
    return render(request, 'team/create_team.html',{
        'form':form
    })    
    
    
@login_required
def detail(request,pk):
    team = get_object_or_404(Team, pk=pk)
    is_member = False
    requests = Request.objects.filter(team=team, accepted = False, declined = False)
    
    if request.user in team.members.all():
        is_member = True
        
    return render(request, 'team/detail.html',{
        'team':team,
        'team_requests':requests,
        'is_member':is_member,
    })    


@login_required
def accept(request,pk, request_id):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    request = get_object_or_404(Request, pk=request_id)
    request.accepted = True
    request.save()
    team.members.add(request.user)
    team.save()
    return redirect('teams:detail',pk=pk)

@login_required
def decline(request,pk, request_id):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    request = get_object_or_404(Request, pk=request_id)
    request.declined = True
    request.save()
    return redirect('teams:detail',pk=pk)