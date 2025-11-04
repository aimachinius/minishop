from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.models import Cart
from review.models import Review
@login_required
def order_create(request):
    cart = Cart.get_user_cart(request)
    if len(cart) == 0:
        messages.error(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            messages.success(request, 'Đặt hàng thành công!')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # Pre-fill form with user profile data
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': profile.phone,
                'address': profile.address,
                'city': profile.city,
                'postal_code': profile.postal_code,
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order/detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    reviewed_product_data = Review.objects.filter(
        user=request.user,
        order__in=orders
    ).values_list('product_id', 'order_id')
    reviewed_product_ids = {
        f"{product_id}_{order_id}" for product_id, order_id in reviewed_product_data
    }
    oders = orders.prefetch_related('items')
    return render(request, 'orders/order/list.html', 
            {'orders': orders,
             'reviewed_product_ids': reviewed_product_ids
            })
    