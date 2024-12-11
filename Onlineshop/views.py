from django.shortcuts import render, redirect

from Onlineshop.models import Produkt
from .forms import ProductForm


# Create your views here.
def produkt_list(request):
    all_produkts = Produkt.objects.all()

    context = {'all_produkts': all_produkts}

    return render(request, 'produkt-list.html', context)

def produkt_detail(request, **kwargs):
    produkt_id = kwargs['pk']
    current_produkt = Produkt.objects.get(id=produkt_id)
    current_user = request.user
    bilder = current_produkt.bilder.all() #Alle Bilder des Produkts

    context = {
        'current_produkt': current_produkt,
        'bilder': bilder,
    }

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


