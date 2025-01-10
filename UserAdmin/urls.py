from django.urls import path
from UserAdmin.views import SignUpView
from . import views
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profil/edit/', views.profil_edit, name='profil_edit'),
    path('profil/', views.profil_view, name='profil_view'),
]