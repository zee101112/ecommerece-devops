from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages

# --- Product views ---
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# --- Register ---
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('product_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Cart functionality ---
def cart_add(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart = request.session.get('cart', {})
        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += 1
        else:
            cart[str(product.id)] = {
                'name': product.name,
                'price': float(product.price),
                'quantity': 1,
            }
        request.session['cart'] = cart
        messages.success(request, f"Added {product.name} to cart.")
        return redirect('cart_detail')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('product_list')

def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('cart_detail')

# views.py
def cart_detail(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart': cart, 'total': total})

from django.shortcuts import redirect, get_object_or_404
from .models import Product

def cart_update(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)

        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
        else:
            cart.pop(str(product_id), None)  # remove if quantity <= 0

        request.session['cart'] = cart
    return redirect('cart_detail')


from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('product_list')

    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total=total)
        for key, item in cart.items():
            product = Product.objects.get(id=int(key))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
        request.session['cart'] = {}  # clear cart after order
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('product_list')

    return render(request, 'shop/checkout.html', {'cart': cart, 'total': total})
