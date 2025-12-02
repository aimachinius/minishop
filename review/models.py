# from django.db import models
# from django.contrib.auth.models import User
# from products.models import Product
# class Review(models.Model):
#     RATING_CHOICES = [
#         (1, '1 - Rất tệ'),
#         (2, '2 - Tệ'),
#         (3, '3 - Bình thường'),
#         (4, '4 - Tốt'),
#         (5, '5 - Rất tốt'),
#     ]   
    
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Đánh giá")
#     comment = models.TextField(blank=True, verbose_name="Bình luận")
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('product', 'user','order')
#         verbose_name = "Đánh giá"
#         verbose_name_plural = "Đánh giá"
    
#     def __str__(self):
#         return f'{self.product.name} - {self.rating} sao'

from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import FileExtensionValidator

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


class ReviewMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Hình ảnh'),
        ('video', 'Video'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='media_files')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(
        upload_to='reviews/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'webm']
            )
        ],
        verbose_name="File"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Media đánh giá"
        verbose_name_plural = "Media đánh giá"
    
    def __str__(self):
        return f'{self.review.product.name} - {self.media_type}'
    
    def save(self, *args, **kwargs):
        # Tự động xác định loại media dựa trên extension
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                self.media_type = 'image'
            elif ext in ['mp4', 'avi', 'mov', 'webm']:
                self.media_type = 'video'
        super().save(*args, **kwargs)