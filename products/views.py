from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q
from decimal import Decimal
from django.core.paginator import Paginator


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # GET request values
    search_query = request.GET.get('q')
    selected_categories = request.GET.getlist('category')
    sort = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    page_size = request.GET.get('page_size', 12)  # default: 12 products per page

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
    elif sort == "rating_desc":
        products = products.order_by("-rating")

    # PAGINATION
    paginator = Paginator(products, int(page_size))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,   # paginated products
        "page_obj": page_obj,
        "paginator": paginator,

        # filters
        "categories": categories,
        "selected_categories": selected_categories,
        "sort": sort,
        "min_price": min_price,
        "max_price": max_price,
        "page_size": int(page_size),
    }

    return render(request, "products/products.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_detail.html", {"product": product})