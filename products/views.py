from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    matched_categories = []
    
    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality - tìm kiếm tổng quát
    query = request.GET.get('q')
    if query:
        # Tìm các danh mục phù hợp với từ khóa
        matched_categories = Category.objects.filter(
            name__icontains=query
        )
        
        # Tìm sản phẩm theo tên, mô tả, hoặc thuộc danh mục có tên chứa từ khóa
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/product/list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'products': page_obj.object_list,
        'query': query,
        'matched_categories': matched_categories,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    # Get reviews and average rating
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'products/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
    })
