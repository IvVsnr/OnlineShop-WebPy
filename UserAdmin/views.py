from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from UserAdmin.forms import BenutzerProfilForm, CustomerUserForm
from UserAdmin.models import BenutzerProfil


class SignUpView(generic.CreateView):
    form_class = CustomerUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        #Speichern des Benutzerformulars
        response = super().form_valid(form)
        #Benutzerprofil erstellen oder bearbeiten
        user = self.object
        try:
            if not hasattr(user, 'profil'):
                BenutzerProfil.objects.create(user=user)
        except Exception as e:
            print(f'Fehler beim Erstellen des Profils: {e}')

        return redirect('profil_edit')

@login_required
def profil_edit(request):
    try:
        profil = request.user.profil
    except BenutzerProfil.DoesNotExist:
        profil = BenutzerProfil(user=request.user)

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
    except BenutzerProfil.DoesNotExist:
        profil:None

    return render(request, 'profil_view.html', {'profil': profil})
