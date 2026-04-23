import os
from django.shortcuts import redirect
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
import jwt
from .utils import build_auth_url , exchange_code_for_tokens , save_tokens ,revoke_token
from .models import Contacts ,Tokens
from .serializers import contact_serializer
from rest_framework.exceptions import PermissionDenied

# Contact Views.
# views related to (view ,edit ,add , delete) contacts from the frontend 

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def contact_list(request):
    contacts = Contacts.objects.filter(user_email=request.user)
    contact_serialized = contact_serializer(contacts, many=True)
    return Response(contact_serialized.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contact_create(request):
    contact_serialized = contact_serializer(data=request.data)
    if contact_serialized.is_valid():
        contact_serialized.save(user_email=request.user)
        return Response(contact_serialized.data, status=201)
    return Response(contact_serialized.errors, status=400)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def contact_update(request, pk):
    try:
        contact = Contacts.objects.get(pk=pk)  
    except Contacts.DoesNotExist:
        return Response(status=404)

    if contact.user_email != request.user:  
        raise PermissionDenied()

    serializer = contact_serializer(contact, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def contact_delete(request, pk):
    try:
        contact = Contacts.objects.get(pk=pk) 
    except Contacts.DoesNotExist:
        return Response(status=404)

    if contact.user_email != request.user: 
        raise PermissionDenied()

    contact.delete()
    return Response(status=204)


# api called by hassan to get the google auth url to show the consent screen to the user 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_google_auth_url(request):
    try:
        auth_url = build_auth_url(request.user)
        return Response({"auth_url": auth_url} , status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# the callback view that google will call after the user give the consent and we will get the code from
# code is passed in the url 
@api_view(['GET'])
def google_callback(request):
    code = request.GET.get("code")
    data = request.GET.get("state")

    if not code:
        return Response({"error": "No code provided"}, status=400)

    try:
        sk = os.getenv("FERNET_KEY")
        if not sk:
            raise ValueError("FERNET_KEY environment variable is not set")
        decoded_data = jwt.decode(data, sk, algorithms=["HS256"])
        user_id = decoded_data.get("user_id")
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid state parameter"}, status=400)

    try:
        tokens_data = exchange_code_for_tokens(code)
        print("tokens_data:", tokens_data)
        save_tokens(user_id, tokens_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)  # ← was unhandled before
    except Exception as e:
        return Response({"error": "Token exchange failed", "detail": str(e)}, status=500)

    return redirect("https://romee-lake.vercel.app/") 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_connected(request):
    user = request.user

    token = Tokens.objects.filter(user=user).first()

    if not token:
        return Response({
            "is_connected": False
        })

    return Response({
        "is_connected": True,
        "email": token.email
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def disconnect(request):
    user = request.user

    token = Tokens.objects.filter(user=user).first()
    
    if not token:
        return Response({"message": "Already disconnected"}, status=200)
    
    try:
        # 🔥 revoke refresh token
        if token.refresh_token:
            revoke_token(token.refresh_token)
            print("token revoked from google api")


    except Exception as e:
        print("Revoke error:", str(e))

    # 🧹 delete from DB
    token.delete()
    print("token deleted from db")

    return Response({"message": "Disconnected successfully"})

