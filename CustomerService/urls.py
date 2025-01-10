
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.DashboardView.as_view(), name='customer_service_dashboard'),
    path('products/', views.ProduktListView.as_view(), name='customer_service_product_list'),
    path('products/<int:pk>/edit/', views.ProduktEditView.as_view(), name='customer_service_product_edit'),
    path('profile/', views.ProfileView.as_view(), name='customer_service_profile_view'),
]