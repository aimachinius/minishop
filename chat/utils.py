from django.contrib.auth.models import User
from .models import Conversation
def choose_superuser():
    """Chọn superuser tiếp theo để gán khi tạo conversation mới"""
    superusers = list(User.objects.filter(is_superuser=True, is_active=True).order_by('id'))
    if not superusers:
        return None

    last_conv = Conversation.objects.exclude(receiver=None).order_by('-id').first()
    if last_conv and last_conv.receiver:
        try:
            index = superusers.index(last_conv.receiver)
            next_index = (index + 1) % len(superusers)
        except ValueError:
            next_index = 0
    else:
        next_index = 0

    return superusers[next_index]
