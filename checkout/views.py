from django.shortcuts import render

from shopping_cart.cart import Cart

from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    variant=item.get("variant"),
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            return render(request, "checkout/created.html", {"order": order})
    else:
        form = OrderCreateForm()
    return render(request, "checkout/create.html", {"cart": cart, "form": form})
