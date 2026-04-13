from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from chat.models import Chats
from chat.agent import message_agent
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # make  the end point allowed to authenticated users
def send_message(request):
    chat_id = request.data.get('chat_id') # catch the chat_id will be sent by frontend developer in JSON 'in request' , if it not catched -> chat_id=none
    user_message = request.data.get('message') # catch the user message 

    if not user_message:
        return Response({"error": "Message is required"}, status=400)


    if not chat_id: # means that -> if chat_id = none -> create a new chat
        chat = Chats.objects.create(
            user_email=request.user,
            message=[]
        )
    else:
        chat = get_object_or_404(
            Chats,
            id=chat_id, # to catch a specific chat
            user_email=request.user # to be sure this chat owned by this user
        )

    chat.message.append({
        "role": "user",
        "content": user_message
    })
    try:
        response = message_agent(chat.message) # it sends all chat to the agent and receive the response from it
    except Exception as e:
        print(f"Agent error: {e}")  #show the error in the terminal to know what is the problem "For debugging only"
        return Response({"error": "Agent failed, try again"}, status=500)
    chat.message.append({
        "role": "assistant",
        "content": response
    })
    chat.save()
    return Response({
        "response": response,
        "chat_id": chat.id,
        "messages": chat.message 
    })

