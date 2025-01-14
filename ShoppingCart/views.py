from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem


def show_shopping_cart(request):

    def create_context_object(
            _shopping_cart_is_empty=True,
            _shopping_cart_items=None,
            _total=0.0
    ):
        """
        Re-usable custom method to create a context for the shopping cart.
        """
        return {
            'shopping_cart_is_empty': _shopping_cart_is_empty,
            'shopping_cart_items': _shopping_cart_items,
            'total': Decimal(_total)  # The model expects a Decimal, not float!
        }

    if request.method == 'POST':

        if 'empty' in request.POST:

            ShoppingCart.objects.get(myuser=request.user).delete()

            context = create_context_object()

        elif 'pay' in request.POST:

            return redirect('shopping-cart-pay')

    else:  # request.method == 'GET'

        myuser = request.user

        if myuser.is_authenticated:

            try:
                shopping_cart = ShoppingCart.objects.get(myuser=myuser)
                shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
                total = shopping_cart.get_total()

                context = create_context_object(
                    _shopping_cart_is_empty=False,
                    _shopping_cart_items=shopping_cart_items,
                    _total=total
                )
            except ObjectDoesNotExist:  # User has no shopping cart
                context = create_context_object()

        else:
            context = create_context_object()

    return render(request, 'shopping-cart.html', context)


@login_required(login_url='/useradmin/login/')
def pay(request):

    def create_context_object(
            _shopping_cart_is_empty=True,
            _payment_form=None,
            _paid=False
    ):
        return {
            'shopping_cart_is_empty': _shopping_cart_is_empty,
            'payment_form': _payment_form,
            'paid': _paid
        }

    if request.method == 'POST':

        myuser = request.user
        form = PaymentForm(request.POST)
        form.instance.myuser = myuser

        if form.is_valid():
            form.save()

            # Empty the shopping cart after payment
            ShoppingCart.objects.get(myuser=myuser).delete()

            context = create_context_object(_paid=True)
        else:
            print(form.errors)
            context = create_context_object()

    else:  # request.method == 'GET'

        try:
            shopping_cart = ShoppingCart.objects.get(myuser=request.user)
            total_payment = Decimal(shopping_cart.get_total())  # The model expects a Decimal, not float!
            payment_form = PaymentForm(initial={'amount': total_payment})

            context = create_context_object(
                _shopping_cart_is_empty=False,
                _payment_form=payment_form
            )
        except ObjectDoesNotExist:
            context = create_context_object()

    return render(request, 'pay.html', context)
