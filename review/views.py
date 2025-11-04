from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from products.models import Product
from orders.models import Order
# Create your views here.
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product,id=product_id)
    orders = Order.objects.filter(user=request.user, items__product=product).first()
    if Review.objects.filter(product=product, user=request.user,order = orders).exists():
        messages.info(request, "Bạn đã đánh giá sản phẩm này rồi.")
        return redirect('products:product_detail', id=product.id, slug=product.slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.order = orders
            review.save()
            messages.success(request, "Cảm ơn bạn đã đánh giá sản phẩm!")
            return redirect('orders:order_list')
    else:
        form = ReviewForm()
    return render(request, 'products/review_form.html',
            {'form':form,
            'product':product
            })