from django.urls import path, re_path
from .views import StartChatView, SendMessageView, GetMessagesView

urlpatterns = [
    path('start-chat/', StartChatView.as_view(), name='start-chat'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('<int:chatroom_id>/history/', GetMessagesView.as_view(), name='get-messages'),
    path('history/', GetMessagesView.as_view(), name='get-messages-all'),
]