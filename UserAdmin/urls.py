from django.urls import path
from UserAdmin.views import SignUpView
urlpatterns = [
path('signup/', SignUpView.as_view(), name='signup'),
]