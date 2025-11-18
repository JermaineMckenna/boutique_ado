from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from decimal import Decimal

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # GET request values
    search_query = request.GET.get('q')
    selected_categories = request.GET.getlist('category')
    sort = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Search filtering
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Category filtering
    if selected_categories:
        products = products.filter(category__name__in=selected_categories)

    # Price range filtering
    if min_price:
        products = products.filter(price__gte=Decimal(min_price))
    if max_price:
        products = products.filter(price__lte=Decimal(max_price))

    # Sorting
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "name_asc":
        products = products.order_by("name")
    elif sort == "name_desc":
        products = products.order_by("-name")

    context = {
        "products": products,
        "categories": categories,
        "selected_categories": selected_categories,
        "sort": sort,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(request, "products/products.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})
