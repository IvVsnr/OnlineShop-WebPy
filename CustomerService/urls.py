from django.urls import path
from . import views

urlpatterns = [
    path('delete/<int:comment_id>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('edit/<int:comment_id>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('editdelete/<int:comment_id>/', views.comment_edit_delete, name='comment-edit-delete'),
    path('dashboard', views.DashboardView.as_view(), name='customer_service_dashboard'),
    path('products/', views.ProduktListView.as_view(), name='customer_service_product_list'),
    path('products/<int:pk>/edit/', views.ProduktEditView.as_view(), name='customer_service_product_edit'),
    path('profile/', views.ProfileView.as_view(), name='customer_service_profile_view'),
    path('editprodukt/<int:pk>/', views.ProduktEdit.as_view(), name='customer_service_produkt_edit'),

]