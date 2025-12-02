from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_with_store, name='chat_with_store'),

    path('user/', views.user_conversation_list, name='user_conversation_list'),

    path('admin/', views.admin_conversation_list, name='admin_conversation_list'),

    path('admin/<int:conversation_id>/', views.admin_chat, name='admin_chat'),
]
