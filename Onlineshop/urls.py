from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.produkt_list, name='produkt-list'),
    path('show/<int:pk>/', views.produkt_detail, name='produkt-detail'),
    path('add/', views.produkt_add, name='produkt-add'),
    path('delete/<int:pk>/', views.produkt_delete, name='produkt-delete'),
]
