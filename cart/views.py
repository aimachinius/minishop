from django.shortcuts import render, redirect, get_object_or_404 
from django.views.decorators.http import require_POST
from products.models import Product
# from .cart import Cart
from .forms import CartAddProductForm
from .models import Cart as CartModel
from django.contrib.auth.decorators import login_required
@require_POST
@login_required
def cart_add(request, product_id):
    cart = CartModel.get_user_cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                # override_quantity=cd['override'])
                override_quantity=False) # false -> tang gia tri
    return redirect('cart:cart_detail')

@require_POST
@login_required
def cart_remove(request, product_id):
    cart = CartModel.get_user_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    print('call remove')
    return redirect('cart:cart_detail')
@login_required
def cart_detail(request):
    cart = CartModel.get_user_cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True
        })
    
    return render(request, 'cart/detail.html', {'cart': cart})

@require_POST
@login_required
def cart_update_all(request):
    cart = CartModel.get_user_cart(request)
    
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            try:
                product_id = int(key.split('_')[1])
                quantity = int(value)
                
                product = get_object_or_404(Product, id=product_id)
                
                if quantity == 0:
                    cart.remove(product)
                else:
                    cart.add(product=product, quantity=quantity, override_quantity=True)
            except (ValueError, IndexError):
                continue 
    return redirect('cart:cart_detail')