from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

# Create your views here.

class StartChatView(APIView):
    def post(self, request):
        employer_id = request.data.get('employee_id')
        employee_id = request.data.get('employer_id')
        
        if employee_id == employer_id:
            return Response({"error": "Employer and Employee cannot be the same user."}, status=status.HTTP_400_BAD_REQUEST)
        if not employer_id or not employee_id:
            return Response({"error": "Both employer_id and employee_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        chat_room, created = ChatRoom.objects.get_or_create(employer_id=employer_id, employee_id=employee_id)
        serializer = ChatRoomSerializer(chat_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
class SendMessageView(APIView):
    def post(self, request):
        chat_room_id = request.data.get('chat_room_id')
        sender_id = request.data.get('sender_id')
        content = request.data.get('content')

        if not chat_room_id or not sender_id or not content:
            return Response({"error": "chat_room_id, sender_id, and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        message = Message.objects.create(chatroom=chat_room, sender_id=sender_id, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetMessagesView(APIView):
    def get(self, request, chatroom_id=None):
        if chatroom_id:
            chat_room = get_object_or_404(ChatRoom, id=chatroom_id)
            messages = Message.objects.filter(chatroom=chat_room).order_by('timestamp')
        else:
            messages = Message.objects.all().order_by('timestamp')
            
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)