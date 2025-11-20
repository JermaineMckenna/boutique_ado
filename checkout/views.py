from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('products')  # Empty cart → send back

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

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total
            order.save()

            # Create line items
            for item in items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    lineitem_total=item["subtotal"]
                )

            # Clear cart
            request.session["cart"] = {}
            return redirect('checkout_success', order_number=order.order_number)
    else:
        form = OrderForm()

    context = {
        "items": items,
        "total": total,
        "form": form,
    }
    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    return render(request, "checkout/success.html", {
        "order": order,
    })

