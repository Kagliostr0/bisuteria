from django.shortcuts import get_object_or_404, redirect, render

from store.models import Product, Variant

from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shopping_cart/detail.html", {"cart": cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        variant = None
        if cd["variant_id"]:
            variant = get_object_or_404(Variant, id=cd["variant_id"], product=product)
        cart.add(
            product=product,
            variant=variant,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )
    return redirect("shopping_cart:cart_detail")


def cart_remove(request, product_id, variant_id=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    variant = None
    if variant_id:
        variant = get_object_or_404(Variant, id=variant_id, product=product)
    cart.remove(product, variant=variant)
    return redirect("shopping_cart:cart_detail")
