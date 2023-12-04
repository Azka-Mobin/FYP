from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='list'),
    path('all/', views.products_list_all, name='list_all'),
    path('add/', views.product_add, name='add'),
    path('<int:pk>/edit/', views.product_edit, name='edit'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
    path('<int:pk>/generate/', views.generate_ad, name='generate_ad'),
    path('<int:pk>/', views.products_detail, name='detail'),

]
