from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for item_id, qty in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = product.price * qty
        total += subtotal

        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": subtotal,
        })

    context = {
        "items": items,
        "total": total,
    }
    return render(request, "cart/cart.html", context)


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    return redirect("view_cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    return redirect("view_cart")


def update_cart(request, product_id):
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except (TypeError, ValueError):
            quantity = 1

        cart = request.session.get("cart", {})

        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            cart.pop(str(product_id), None)

        request.session["cart"] = cart

    return redirect("view_cart")


