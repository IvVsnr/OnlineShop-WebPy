from lib2to3.fixes.fix_input import context

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from Onlineshop.forms import ProductForm
from Onlineshop.models import Produkt
from Onlineshop.views import produkt_list
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from Onlineshop.forms import ProductForm
from Onlineshop.models import Produkt
from UserAdmin.forms import BenutzerProfilForm
from UserAdmin.models import BenutzerProfil


# Dashboardview (Übersicht, die dem Kunden-Service auf den wichtigsten Bereichen der App hinweist)
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

# Produktliste für den Kunden-Service (Zeigt alle Produkt die der Kunden-Service bearbeiten kann)
class ProduktListView(PermissionRequiredMixin, ListView):
    model = Produkt
    template_name = 'produkt_list.html'
    context_object_name = 'produkts'
    permission_required = 'Onlineshop.change_produkt'

# Produktbearbeitung (Kunden-Service kann Prodsukte bearbeiten)
class ProduktEditView(PermissionRequiredMixin, View):
    # Berechtigung für das Bearbeiten von Produkten
    permission_required = ('OnlineShop.EditProdukt')
    # falls keine Berechtigung wird eine 404 geworfen
    raise_exception = True

    def get(self, request, pk):
        produkt = Produkt.objects.get(pk=pk)
        form = ProductForm(instance=produkt)
        return render(request,'produkt_edit.html',{'form':form, 'produkt':produkt})

    def post(self, request, pk):
        produkt = Produkt.objects.get(pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=produkt)
        if form.is_valid():
            form.save()
            return redirect('customer_service_produkt_list')
        return redirect(request, 'produkt_edit.html', {'form':form, 'produkt':produkt})

# Profilansicht
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profil'] = self.request.user.profil
        except BenutzerProfil.DoesNotExist:
            context['profil'] = None
        return context

# Profilbearbeitung
@login_required
def profil_edit(request):
    try:
        profil = request.user.profil
    except BenutzerProfil.DoesNotExist:
        profil = BenutzerProfil(user = request.user)

    if request.method == 'POST':
        form = BenutzerProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('customer_service_profile_view')

    else:
        form = BenutzerProfilForm(instance=profil)

    return render(request, 'profil_edit.html', {'form': form})
