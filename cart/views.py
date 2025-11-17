from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from django.contrib import messages


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session['cart'] = cart
    messages.success(request, f"Added {product.name} to your cart.")

    return redirect('product_detail', product_id=product_id)


def update_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart.pop(str(product_id))

    request.session['cart'] = cart
    return redirect('view_cart')

