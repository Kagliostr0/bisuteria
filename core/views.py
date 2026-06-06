from django.shortcuts import render

from store.models import Product


def home(request):
    products = Product.objects.filter(available=True)[:8]
    return render(request, "core/home.html", {"products": products})


def about(request):
    return render(request, "core/about.html")
