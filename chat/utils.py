from django.contrib.auth.models import User
from .models import Conversation

def choose_superuser(conversation):
    """
    Chọn superuser tiếp theo nhận tin nhắn theo thứ tự tuần tự (round-robin).
    - conversation: instance Conversation hiện tại
    - Trả về: superuser được chọn
    """
    superusers = list(User.objects.filter(is_superuser=True, is_active=True).order_by('id'))
    if not superusers:
        return None

    # Lấy last_receiver từ conversation cuối cùng được tạo
    last_conversation = Conversation.objects.exclude(receiver=None).order_by('-id').first()
    
    if last_conversation and last_conversation.receiver:
        try:
            index = superusers.index(last_conversation.receiver)
            next_index = (index + 1) % len(superusers)
        except ValueError:
            next_index = 0
    else:
        next_index = 0

    selected_superuser = superusers[next_index]

    # Gán receiver cho conversation mới
    conversation.receiver = selected_superuser
    conversation.save()

    return selected_superuser
