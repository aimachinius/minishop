from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Rất tệ'),
        (2, '2 - Tệ'),
        (3, '3 - Bình thường'),
        (4, '4 - Tốt'),
        (5, '5 - Rất tốt'),
    ]   
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Đánh giá")
    comment = models.TextField(blank=True, verbose_name="Bình luận")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user','order')
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
    
    def __str__(self):
        return f'{self.product.name} - {self.rating} sao'