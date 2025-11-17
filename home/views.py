from django.shortcuts import render
from products.models import Product

def index(request):
    trending = Product.objects.all().order_by('-id')[:4]  # newest products

    return render(request, "home/index.html", {
        "trending": trending
    })

