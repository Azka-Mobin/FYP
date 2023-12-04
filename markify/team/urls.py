from django.urls import path
from . import views

app_name = 'teams'
urlpatterns = [
    path('<int:pk>/activate/', views.teams_activate, name='activate'),
    path('<int:pk>/accept/<int:request_id>/', views.accept, name='accept'),
    path('<int:pk>/decline/<int:request_id>/', views.decline, name='decline'),
    path('<int:pk>/edit/', views.edit_team, name='edit'),
    path('<int:pk>/join/', views.join_team, name='join'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create_team, name='create'),
    path('all/', views.list_teams_all, name='list_all'),  
    path('', views.teams_list, name='list'),   
]
