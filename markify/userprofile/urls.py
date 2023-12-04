from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('myaccount/', views.my_account, name='myaccount')
]
