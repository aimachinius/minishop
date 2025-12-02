from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order

@receiver(pre_save, sender=Order)
def update_stock(sender, instance, **kwargs):
    if instance.pk is None:
        return

    old_status = Order.objects.get(pk=instance.pk).status
    new_status = instance.status

    if old_status == new_status:    
        return

    if old_status != "delivered" and new_status == "delivered":
        for item in instance.items.all():
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()

    if old_status == "delivered" and new_status == "cancelled":
        for item in instance.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
