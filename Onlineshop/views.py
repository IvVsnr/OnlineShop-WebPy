from django.shortcuts import render, redirect, get_object_or_404

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
    produkt_bild = current_produkt.produkt_bild


    context = {
        'current_produkt': current_produkt,
        'produkt_bild': produkt_bild,
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


def produkt_delete(request, **kwargs):
    produkt_id = kwargs['pk']
    current_produkt = Produkt.objects.get(id=produkt_id)
    #produkt = get_object_or_404(Produkt, pk=pk)

    if request.method == 'POST':
        current_produkt.delete()
        return redirect('produkt-list')

    return render(request, 'produkt-delete-confirm.html', {'produkt': current_produkt})
