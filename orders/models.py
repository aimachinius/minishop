from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang xử lý'),
        ('processing', 'Đang chuẩn bị'),
        ('shipped', 'Đã giao hàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Người dùng")
    first_name = models.CharField(max_length=50, verbose_name="Họ")
    last_name = models.CharField(max_length=50, verbose_name="Tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.CharField(max_length=250, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, verbose_name="Thành phố")
    postal_code = models.CharField(max_length=20, verbose_name="Mã bưu điện")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Đơn hàng #{self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Sản phẩm")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
