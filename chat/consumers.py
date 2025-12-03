import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Nhận tin từ WebSocket client"""
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        sender_username = data.get('sender_username', 'User')
         

        saved = await self.save_message(self.conversation_id, sender_id, message)
        if not saved:
            await self.send(text_data=json.dumps({
                'error': 'Không thể lưu tin nhắn'
            }))
            return
        created_at_local = timezone.localtime(saved.created_at)
        created_at = created_at_local.strftime('%H:%M')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'sender_username': sender_username,
                'created_at': created_at
            }
        )

    async def chat_message(self, event):
        """Gửi tin ra WebSocket"""
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event.get('sender_username', 'User'),
            'created_at' : event['created_at']
        }))

    async def chat_product(self, event):
        """Gửi sản phẩm ra WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_product',  
            'product': event['product'],
            'sender_id': event['sender_id'],
            'sender_username': event.get('sender_username', 'User'),
            'created_at' : event['created_at']
        }))
    
    @database_sync_to_async
    def save_message(self, conversation_id, sender_id, text):
        """Lưu tin nhắn vào database"""
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            sender = User.objects.get(id=sender_id)
            
            msg = Message.objects.create(
                conversation=conversation,
                sender=sender,
                text=text
            )
            return msg
        except Conversation.DoesNotExist:
            print(f"Conversation {conversation_id} không tồn tại")
            return False
        except User.DoesNotExist:
            print(f"User {sender_id} không tồn tại")
            return False
        except Exception as e:
            print(f"Lỗi lưu tin nhắn: {e}")
            return False