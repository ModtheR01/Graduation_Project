from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from chat.models import Chats
from chat.agent import message_agent
from rest_framework.response import Response
from .utils import generate_title
from threading import Thread
from flights.state_store import get_store

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # make  the end point allowed to authenticated users
def send_message(request):
    chat_id = request.data.get('chat_id') # catch the chat_id will be sent by frontend developer in JSON 'in request' , if it not catched -> chat_id=none
    user_id = request.user.pk
    print("user id in send message",user_id)
    user_message = request.data.get('message') # catch the user message 
    print("user",request.user)
    if not user_message:
        return Response({"error": "Message is required"}, status=400)

    if not chat_id:
        chat = Chats(
            user_email=request.user,
            message=[{"role": "user","content": user_message}],
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

    store= get_store()
    store["chat_id"] = chat.id

    try:
        if not chat_id: 
            Thread(target=generate_title, args=(user_message,chat.id,request.user)).start() # generate title in a separate thread to avoid blocking the main thread
        response = message_agent(user_id,chat.message)
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
        # "title": chat.title,
        "chat_id": chat.id,
        "messages": chat.message 
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_chats(request):
    chats = Chats.objects.filter(user_email=request.user).values('id', 'title')
    if not chats:
        return Response({"error": "No chats found"}, status=404)
    return Response(chats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_by_id(request, chat_id):
    # chat = get_object_or_404(Chats, id=chat_id, user_email=request.user)
    chat = Chats.objects.filter(id=chat_id, user_email=request.user).first()
    if not chat:
        return Response({"error": "Chat not found"}, status=404)
    return Response(chat.message)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    chat = Chats.objects.filter(id=chat_id, user_email=request.user).first()
    if not chat:
        return Response({"error": "Chat not found"}, status=404)
    chat.delete()
    return Response({"message": "Chat deleted successfully"})