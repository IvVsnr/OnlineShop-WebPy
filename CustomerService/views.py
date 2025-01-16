from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, TemplateView

from Onlineshop.forms import ProductForm
from .forms import CommentEditForm, ProductEditForm
from Onlineshop.models import Comment, Produkt
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from UserAdmin.forms import BenutzerProfilForm
from UserAdmin.models import MyUser


# class CommentDeleteView(LoginRequiredMixin, ListView):
#     login_url = '/useradmin/login/'
class CommentDeleteView(ListView):

    model = Comment
    context_object_name = 'all_comments'
    template_name = 'comment-delete.html'

    def get_context_data(self, **kwargs):

        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        myuser = self.request.user

        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()

        return context

    def post(self, request, *args, **kwargs):

        comment_id = request.POST['comment_id']

        if 'delete' in request.POST:
            Comment.objects.get(id=comment_id).delete()

            return redirect('comment-delete')


class CommentEditView(UpdateView):

    model = Comment
    form_class = CommentEditForm
    template_name = 'comment-edit.html'
    success_url = reverse_lazy('comment-delete')

    def get_context_data(self, **kwargs):

        context = super(CommentEditView, self).get_context_data(**kwargs)

        myuser = self.request.user

        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()

        return context

class ProduktEdit(UpdateView):
    model = Produkt
    form_class = ProductEditForm
    template_name = 'produkt_edit.html'
    success_url = reverse_lazy('produkt-list')

    def get_context_data(self, **kwargs):
        context = super(ProduktEdit, self).get_context_data(**kwargs)
        myuser = self.request.user
        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()
        return context

#class ProfileEdit(UpdateView):
#    model = MyUser
#    form_class = BenutzerProfilForm
#    template_name = 'profile_edit.html'
#    success_url = reverse_lazy('produkt-list')

#    def get_context_data(self, **kwargs):
#        context = super(ProfileEdit, self).get_context_data(**kwargs)
#        myuser = self.request.user
#        context

# @staff_member_required(login_url='/useradmin/login/')
def comment_edit_delete(request, comment_id: str):

    if request.method == 'POST':
        print('-------------', request.POST)

        if 'edit' in request.POST:
            form = CommentEditForm(request.POST)

            if form.is_valid():
                comment = Comment.objects.get(id=comment_id)
                new_text = form.cleaned_data['text']
                comment.text = new_text
                comment.save()

        elif 'delete' in request.POST:
            Comment.objects.get(id=comment_id).delete()

        return redirect('comment-delete')

    else:  # GET case

        comment = Comment.objects.get(id=comment_id)
        form = CommentEditForm(request.POST or None, instance=comment)

        myuser = request.user
        has_delete_permission = not myuser.is_anonymous and myuser.has_delete_permission()

        context = {
            'form': form,
            'comment': comment,
            'has_delete_permission': has_delete_permission,
        }

        return render(request, 'comment-edit-delete.html', context)

#########
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
        except MyUser.DoesNotExist:
            context['profil'] = None
        return context

# Profilbearbeitung
@login_required
def profil_edit(request):
    try:
        profil = request.user.profil
    except MyUser.DoesNotExist:
        profil = MyUser(user = request.user)

    if request.method == 'POST':
        form = BenutzerProfilForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('customer_service_profile_view')

    else:
        form = BenutzerProfilForm(instance=profil)

    return render(request, 'profil_edit.html', {'form': form})


class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser-list.html'

    def get_success_url(self):
        return reverse_lazy('customer_service_user_list')