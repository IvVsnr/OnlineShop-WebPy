from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.produkt_list, name='produkt-list'),
    path('show/<int:pk>/', views.produkt_detail, name='produkt-detail'),
    path('add/', views.produkt_add, name='produkt-add'),
    path('delete/<int:pk>/', views.produkt_delete, name='produkt-delete'),
    path('show/<int:pk>/vote/<str:up_or_down>/', views.vote, name='produkt-vote'),
    path('show/<int:pk>/meldung/<str:melden>/', views.meldung, name='produkt-melden'),
    path('confirm_meldung/<str:pk>/', views.meldung, name='confirm-meldung'),
    path('search/', views.produkt_search, name='produkt-search'),
    path('delete/', views.BewertungDeleteView.as_view(), name='bewertung-delete'),
    path('editdelete/<int:comment_id>/', views.bewertung_edit_delete, name='comment-edit-delete'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/edit/<int:pk>', views.ProfileEdit.as_view(), name='profile-edit'),
]
