from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .models import Contacts
from serializers import contact_serializer
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

# functions for the ai function call
# to do 


