from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        "store/product_list.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, category_slug=None, slug=None):
    if not slug:
        slug = category_slug
        category_slug = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, category=category, slug=slug, available=True)
    else:
        product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "store/product_detail.html", {"product": product})
