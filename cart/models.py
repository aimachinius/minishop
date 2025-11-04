from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from .forms import CartAddProductForm
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', verbose_name="Người dùng")

    def get_user_cart(request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    def add(self, product, quantity=1, override_quantity=False):
        item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if override_quantity:
            item.quantity = quantity
        else:
            if item.quantity == 1:
                item.quantity = quantity
            else:
                item.quantity += quantity
        item.save()

    def remove(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

    def clear(self):
        self.items.all().delete()

    def __len__(self):
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __iter__(self):
        for item in self.items.select_related('product'):
            
            yield {
                "product": item.product,
                "quantity": item.quantity,
                "price": item.product.price,
                "total_price": item.product.price * item.quantity,
                "update_quantity_form": CartAddProductForm(initial={
                "quantity": item.quantity,
                "override": True
            })
            }

    class Meta:
        ordering = ['user']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="Giỏ hàng")
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
