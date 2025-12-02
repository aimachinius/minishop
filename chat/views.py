from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from products.models import Product
from .models import Conversation, Message
from .utils import choose_superuser
from django.db.models import Max


@login_required
def chat_with_store(request):
    user = request.user
    product = None

    product_id = request.POST.get('product_id') or request.GET.get('product_id')
    if product_id:
        product = get_object_or_404(Product, id=product_id)

    conversation = Conversation.objects.filter(sender=user).first()
    if not conversation:
        selected_superuser = choose_superuser()
        conversation = Conversation.objects.create(sender=user, receiver=selected_superuser)

    if product:
        if not conversation.messages.filter(product=product).exists():
            Message.objects.create(
                conversation=conversation,
                sender=user,
                product=product
            )

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text or product_id:
            Message.objects.create(
                conversation=conversation,
                sender=user,
                text=text if text else None,
                product=product
            )
        return redirect('chat:chat_with_store')

    messages = conversation.messages.select_related("sender").order_by('created_at')

    return render(request, 'chat/chat.html', {
        'conversation': conversation,
        'messages': messages,
        'product': product
    })



@admin_required
def admin_chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, receiver=request.user)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
        return redirect('chat:admin_chat', conversation_id=conversation.id)

    messages = conversation.messages.select_related("sender").order_by('created_at')

    return render(request, 'chat/admin_chat.html', {
        'conversation': conversation,
        'messages': messages
    })


@login_required
def user_conversation_list(request):
    user = request.user
    conversations = (
        Conversation.objects.filter(sender=user)
        .annotate(last_msg=Max('messages__created_at'))
        .order_by('-last_msg')
    )
    return render(request, 'chat/user_conversation_list.html', {
        'conversations': conversations
    })


@admin_required
def admin_conversation_list(request):
    admin = request.user
    conversations = (
        Conversation.objects.filter(receiver=admin)
        .annotate(last_msg=Max('messages__created_at'))
        .order_by('-last_msg')
    )
    return render(request, 'chat/admin_conversation_list.html', {
        'conversations': conversations
    })
