from math import floor

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from Onlineshop.models import Produkt, Comment
from .forms import ProductForm, SearchForm, CommentForm, CommentEditForm
from django.contrib import messages
from django.views.generic import ListView, UpdateView


# Create your views here.
def produkt_list(request):
    all_produkts = Produkt.objects.all()

    context = {'all_produkts': all_produkts}

    return render(request, 'produkt-list.html', context)


def vote(request, pk: str, up_or_down: str):
    if not request.user.is_authenticated:
        messages.error(request, "Bitte melden Sie sich an, um abzustimmen.")
        return redirect('login')
    user = request.user

    try:
        comment = Comment.objects.get(id=pk)
        success = comment.vote(user, up_or_down)
        if not success:
            messages.error(request, "Sie haben die Bewertung bereits bewertet!")
        else:
            messages.error(request, "Sie haben die Bewertung neu bewertet!")
    except Comment.DoesNotExist:
        print("Comment not found.")

    return redirect('produkt-detail', pk=comment.produkt.pk)

def meldung(request, pk: str, melden: str):
    if not request.user.is_authenticated:
        messages.error(request, "Bitte melden Sie sich an, um abzustimmen.")
        return redirect('login')
    user = request.user
    try:
        comment = Comment.objects.get(id=pk)
        success = comment.meld(user, melden)
        if not success:
            messages.error(request, "Sie haben die Bewertung bereits gemeldet!")
        else:
            messages.error(request, "Sie haben die Bewertung gemeldet!")
    except Comment.DoesNotExist:
        print("Comment not found.")

    return redirect('produkt-detail', pk=comment.produkt.pk)

def produkt_detail(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    produkt_id = kwargs['pk']
    current_produkt = Produkt.objects.get(id=produkt_id)
    current_user = request.user
    produkt_bild = current_produkt.produkt_bild

    # Durchschnittsbewertung abrufen und Sterne vorbereiten
    durchschnittsbewertung = floor(current_produkt.durchschnittsterne())
    total_stars = 5  # Anzahl der Sterne
    sterne_bewertung = ['★' if i < durchschnittsbewertung else '☆' for i in range(total_stars)]

    comments = Comment.objects.filter(produkt=current_produkt)
    #bewertungen = Bewertung.objects.filter(produkt=current_produkt)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.user = current_user
        comment_form.instance.produkt = current_produkt

        # Prüfen, ob der Benutzer bereits eine Bewertung für dieses Produkt abgegeben hat
        if Comment.objects.filter(user=current_user, produkt=current_produkt).exists():
            messages.error(request, "Sie haben dieses Produkt bereits bewertet und haben einen Kommentar hinterlassen!")
            return redirect('produkt-detail', pk=produkt_id)

        if comment_form.is_valid():
            comment_form.save()
            return redirect('produkt-detail', pk=produkt_id)
        else:
            print(comment_form.errors)

        # Bewertung-Formular-Logik
        if request.method == 'POST':
            bewertung_form = CommentForm(request.POST)
            bewertung_form.instance.user = current_user
            bewertung_form.instance.produkt = current_produkt

            if bewertung_form.is_valid():
                bewertung_form.save()
                return redirect('produkt-detail', pk=produkt_id)
            else:
                print(bewertung_form.errors)

    context = {
        'current_produkt': current_produkt,
        'comments_on_the_produkt': comments,
        'bewertungen_on_the_produkt': comments,
        'produkt_bild': produkt_bild,
        'sterne_bewertung': sterne_bewertung,
        'comment_form': CommentForm,
        'bewertung_form': CommentForm
    }
#Funktioniert soweit nur noch, exeption wenn man schon bewertet hat hinzufügen, ansosnten noch hilfreich oder nicht hinzufügen.
    return render(request, 'produkt-detail.html', context)

def produkt_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.instance.user = request.user

        if form.is_valid():
            form.save()
            print('Saved a new Produkt in DB')
            return redirect('produkt-list')
        else:
            print(form.errors)

        #return redirect('produkt-list')
    else:
        form = ProductForm()
        #context = {'form': form_my}
        return render(request, 'produkt-add.html', {'form': form})


def produkt_delete(request, **kwargs):
    produkt_id = kwargs['pk']
    current_produkt = Produkt.objects.get(id=produkt_id)
    #produkt = get_object_or_404(Produkt, pk=pk)

    if request.method == 'POST':
        current_produkt.delete()
        return redirect('produkt-list')

    return render(request, 'produkt-delete-confirm.html', {'produkt': current_produkt})


def produkt_search(request):

    if request.method == 'POST':

        search_string_name = request.POST['name']
        search_string_preis = request.POST['preis']
        searched_preis = int(search_string_preis) if search_string_preis else 0
        search_string_beschreibung = request.POST['beschreibung']
        search_string_sterne = request.POST['sterne']

        produkt_found = Produkt.objects.filter(
            Q(name__exact=search_string_name)
            & Q(beschreibung__contains=search_string_beschreibung)
            | Q(preis__exact=searched_preis)
            #& Q(sterne__exact=search_string_sterne)
        )

        if search_string_sterne:
            search_sterne = int(search_string_sterne)
            produkt_found = [
                produkt for produkt in produkt_found
                if produkt.durchschnittsterne() == search_sterne
            ]

        # alternative für stern suche:
        #if search_string_sterne:
        #    search_sterne = int(search_string_sterne)
        #    produkt_found = produkt_found.annotate(
        #        durchschnitt_sterne=Avg('bewertungen__sterne')
        #    ).filter(durchschnitt_sterne__gte=search_sterne)

        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': True,
            'form': form_in_function_based_view,
            'produkt_found': produkt_found,
            #'produkt_foundd': produkt_foundd,
        }

    else:  # GET

        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': False,
            'form': form_in_function_based_view,
        }

    return render(request, 'produkt-search.html', context)

class BewertungDeleteView(ListView):

    model = Comment
    context_object_name = 'all_comments'
    template_name = 'comment-delete.html'

    def get_context_data(self, **kwargs):

        context = super(BewertungDeleteView, self).get_context_data(**kwargs)
        myuser = self.request.user
#Funktioniert also der edit, nur noch delete und halt dass der user es nur machen kann wenn er auch den commentar verfasst hat
        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()

        return context

    def post(self, request, *args, **kwargs):

        comment_id = request.POST['comment_id']

        if 'delete' in request.POST:
            Comment.objects.get(id=comment_id).delete()

            return redirect('bewertung-delete')

def bewertung_edit_delete(request, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user) #dadurch kann nur der user edit/delete machen wenn der comment ihm gehört

    if request.method == 'POST':
        print('-------------', request.POST)

        if 'edit' in request.POST:
            form = CommentEditForm(request.POST, instance=comment)

            if form.is_valid():
                comment = Comment.objects.get(id=comment_id)
                new_text = form.cleaned_data['text']
                new_sterne = form.cleaned_data['sterne']
                comment.text = new_text
                comment.sterne = new_sterne
                comment.save()

        elif 'delete' in request.POST:
            Comment.objects.get(id=comment_id).delete()

        return redirect('produkt-list')

    else:  # GET case

        comment = Comment.objects.get(id=comment_id)
        form = CommentEditForm(request.POST or None, instance=comment)

        context = {
            'form': form,
            'comment': comment,
        }

        return render(request, 'bewertung-edit-delete.html', context)