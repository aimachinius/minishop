from django.db import models
from django.contrib.auth.models import User
from products.models import Product  

class Conversation(models.Model):
    # Người gửi đầu tiên (user bình thường)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_sent')
    # Người nhận tin nhắn (sẽ là superuser, luân phiên)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_received')
    last_receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_received')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} from {self.sender.username} to {self.receiver.username}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.sender.username} sent a product: {self.product.name}"
        return f"{self.sender.username}: {self.text}"


