from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal

from products.models import Product
from cart.views import view_cart  # not required, but fine
from .forms import OrderForm
from .models import Order, OrderLineItem


def _cart_to_context(request):
    cart = request.session.get("cart", {})
    items = []
    total = Decimal("0.00")

    for product_id, qty in cart.items():
        product = Product.objects.get(pk=product_id)
        subtotal = product.price * qty

        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": subtotal,
        })

        total += subtotal

    return items, total


def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect("products")

    items, total = _cart_to_context(request)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total
            order.save()

            # Save line items
            for item in items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    lineitem_total=item["subtotal"]
                )

            # Clear cart
            request.session["cart"] = {}

            return redirect("checkout_success", order.id)

        else:
            messages.error(request, "Please check your form details.")
    else:
        form = OrderForm()

    return render(request, "checkout/checkout.html", {
        "form": form,
        "items": items,
        "total": total,
    })


def checkout_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "checkout/checkout_success.html", {"order": order})

