
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

from Onlineshop.models import Comment
from .forms import MySignUpForm, BenutzerProfilForm, UserRechte
from .models import MyUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

class SignUpView(generic.CreateView):
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

        return HttpResponseRedirect(self.get_success_url())

@login_required #so überarbeiten dass wenn man user ist, der user sein profil updaten kann
def profil_edit(request):
   try:
       profil = request.MyUser.profil
   except MyUser.DoesNotExist:
       profil = MyUser(user=request.user)

   if request.method == 'POST':
       form = BenutzerProfilForm(request.POST, request.FILES, instance=profil)
       if form.is_valid():
           form.save()
           return redirect('produkt-list')
   else:
       form = BenutzerProfilForm(instance=profil)

   return render(request, 'profil_edit.html', {'form': form})

@login_required
def profil_view(request):

   try:
       profil = request.user.profil
   except MyUser.DoesNotExist:
       profil:None

   return render(request, 'profil_view.html', {'profil': profil})

class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser-list.html'

def rechte_zuweisen(request, user_id):
    user_to_edit = get_object_or_404(MyUser, id=user_id)

    if request.method == 'POST':
        form = UserRechte(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('myuser_list')  # Anpassen: Zielseite nach Speicherung
    else:
        form = UserRechte(instance=user_to_edit)

    context = {
        'form': form,
        'user_to_edit': user_to_edit
    }
    return render(request, 'rechte-zuweisung.html', context)

def delete_user(request, user_id):
    user_to_delete = get_object_or_404(MyUser, id=user_id)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('myuser_list')  # Nach dem Löschen zur Benutzerliste zurückkehren
    return render(request, 'confirm-delete.html', {'user': user_to_delete})

def delete_comment(request, comment_id):
    comment_to_delete = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment_to_delete.delete()
        return redirect('produkt-list')  # Nach dem Löschen zur Benutzerliste zurückkehren
    return render(request, 'confirm-comment-delete.html', {'comment': comment_to_delete})