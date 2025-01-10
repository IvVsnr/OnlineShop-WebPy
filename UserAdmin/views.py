from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import MySignUpForm
from .models import MyUser


class MySignUpView(generic.CreateView):

    form_class = MySignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyLoginView(LoginView):

    template_name = 'registration/login.html'

    def form_valid(self, form):
        """
        At this point the security check complete.
        The user gets logged in here the user in
        and custom code gets performed.
        """
        auth_login(self.request, form.get_user())
        form.get_user().execute_after_login()  # custom code

        return HttpResponseRedirect(self.get_success_url())