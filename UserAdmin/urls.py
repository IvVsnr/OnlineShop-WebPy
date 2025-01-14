from django.urls import path
#from UserAdmin.views import SignUpView
from . import views
from .views import SignUpView

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    #path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    #path('profil/edit/', views.profil_edit, name='profil_edit'),
    #path('profil/', views.profil_view, name='profil_view'),
    path('show_myusers/', views.MyUserListView.as_view(), name='myuser_list'),
    path('rechte_zuweisen/<int:user_id>/', views.rechte_zuweisen, name='rechte-zuweisung'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete-user'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
]