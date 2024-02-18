from cart.cart import Cart
from .models import OrderItem
from django.urls import reverse
from .forms import OrderCreateForm
from django.shortcuts import render, redirect

from .tasks import order_created
# Create your views here.


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Save the collected customer's information
            order = form.save()

            # Create an order
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            # clear the cart for checkout
            cart.clear()

            # Add asynchronous task
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
