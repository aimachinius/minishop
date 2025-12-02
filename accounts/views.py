from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Profile
from .forms import UserProfileForm
from .decorators import admin_required, superuser_required
from orders.models import Order
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, f'Tạm biệt {request.user.username}! Bạn đã đăng xuất thành công.')
        return super().dispatch(request, *args, **kwargs)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'orders': orders
    })


# ======================== ADMIN VIEWS ========================

@admin_required
def admin_dashboard(request):
    """Dashboard tổng quan dành cho admin"""
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = total_users - active_users
    admin_users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    return render(request, 'accounts/admin/dashboard.html', {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'admin_users': admin_users,
        'recent_users': recent_users,
    })


@admin_required
def admin_user_list(request):
    """Danh sách tất cả khách hàng cho admin"""
    users = User.objects.all().annotate(
        order_count=Count('orders')
    ).order_by('-date_joined')
    
    # Tìm kiếm
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    
    # Lọc theo trạng thái
    status = request.GET.get('status')
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)
    elif status == 'admin':
        users = users.filter(Q(is_staff=True) | Q(is_superuser=True))
    
    # Phân trang
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/admin/user_list.html', {
        'page_obj': page_obj,
        'users': page_obj.object_list,
        'query': query,
        'status': status,
    })


@admin_required
def admin_user_detail(request, user_id):
    """Chi tiết thông tin khách hàng cho admin"""
    user = get_object_or_404(User, id=user_id)
    
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    # Lấy đơn hàng của user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    # Thống kê
    total_orders = orders.count()
    total_spent = sum(order.get_total_cost() for order in orders)
    
    return render(request, 'accounts/admin/user_detail.html', {
        'user': user,
        'profile': profile,
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    })


@admin_required
def admin_toggle_user_status(request, user_id):
    """Kích hoạt/vô hiệu hóa tài khoản user"""
    user = get_object_or_404(User, id=user_id)
    
    # Không cho phép admin tự vô hiệu hóa chính mình
    if user.id == request.user.id:
        messages.error(request, 'Bạn không thể vô hiệu hóa tài khoản của chính mình!')
        return redirect('accounts:admin_user_detail', user_id=user_id)
    
    # Không cho phép vô hiệu hóa superuser trừ khi là superuser
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Chỉ superuser mới có thể vô hiệu hóa tài khoản superuser khác!')
        return redirect('accounts:admin_user_detail', user_id=user_id)
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status_text = "kích hoạt" if user.is_active else "vô hiệu hóa"
        messages.success(request, f'Đã {status_text} tài khoản {user.username} thành công!')
        
        return redirect('accounts:admin_user_detail', user_id=user_id)
    
    return render(request, 'accounts/admin/confirm_toggle_status.html', {
        'user': user,
    })


@superuser_required
def admin_create_staff(request):
    """Tạo tài khoản admin mới (chỉ superuser)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  
            user.is_superuser = True
            user.save()
            
            messages.success(request, f'Tạo tài khoản admin {user.username} thành công!')
            return redirect('accounts:admin_user_detail', user_id=user.id)
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/admin/create_staff.html', {
        'form': form,
    })
