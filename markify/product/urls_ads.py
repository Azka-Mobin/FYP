from django.urls import path
from . import views

app_name = 'ads'


urlpatterns = [
    path('<int:pk>/delete', views.ad_delete, name='delete'),
    path('<int:pk>/add-to-campaign', views.ad_add_campaign, name='add-to-campaign'),
    path('<int:pk>/', views.ad_detail, name='detail'),
    path('', views.ad_list, name='list'),
    
]
