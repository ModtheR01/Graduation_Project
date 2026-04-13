from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from chat.models import Chats
from chat.agent import message_agent
from rest_framework.response import Response
from .utils import generate_title
from threading import Thread

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # make  the end point allowed to authenticated users
def send_message(request):
    chat_id = request.data.get('chat_id') # catch the chat_id will be sent by frontend developer in JSON 'in request' , if it not catched -> chat_id=none
    user_message = request.data.get('message') # catch the user message 
    print("user",request.user)
    if not user_message:
        return Response({"error": "Message is required"}, status=400)

    if not chat_id:
        chat = Chats(
            user_email=request.user,
            message=[{
                "role": "user",
                "content": user_message
            }],
        )
        chat.save()
    else:
        chat = get_object_or_404(
            Chats,
            id=chat_id,
            user_email=request.user
        )

        messages = chat.message or []
        messages.append({
            "role": "user",
            "content": user_message
        })
        chat.message = messages


    try:
        if not chat_id: 
            Thread(target=generate_title, args=(user_message,chat.id,request.user)).start() # generate title in a separate thread to avoid blocking the main thread

        response = message_agent(chat.message)
    except Exception as e:
        print(f"Agent error: {e}")
        return Response({"error": "Agent failed, try again"}, status=500)
    
    chat.message.append({
        "role": "assistant",
        "content": response
    })
    Chats.objects.filter(id=chat.id).update(message=chat.message)
    return Response({
        "response": response,
        "chat_id": chat.id,
        "messages": chat.message 
    })
