from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
import jwt
from .models import ToDoItems,ToDoList
from .serializers import todoList_items_serializer,todoList_serializer


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_lists(request):
    user = request.user
    todo_lists = ToDoList.objects.filter(user = user)
    if todo_lists:
        serialized_todo_lists = todoList_serializer(todo_lists, many=True)
        return Response({"data":serialized_todo_lists.data} ,status=200)
    return Response({"error": "there is no available lists for this user "})

@api_view(['POST'])
def create_list_view(request):
    user = request.user
    list_name = request.data.get("list_name")

    if not list_name:
        return Response({"error": "list_name is required"}, status=400)

    if ToDoList.objects.filter(user=user, list_name=list_name).exists():
        return Response({"error": "list already exists"}, status=400)

    ToDoList.objects.create(user=user, list_name=list_name)

    return Response({
        "status": "created",
        "list_name": list_name
    })

@api_view(['DELETE'])
def delete_list_view(request):
    user = request.user
    list_name = request.data.get("list_name")

    if not list_name:
        return Response({"error": "list_name is required"}, status=400)

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=list_name)
    except ToDoList.DoesNotExist:
        return Response({"error": "list not found"}, status=404)

    todo_list.delete()

    return Response({
        "status": "deleted",
        "list_name": list_name
    })

@api_view(['GET'])
def get_items_in_list(request, list_name):
    user = request.user

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=list_name)
    except ToDoList.DoesNotExist:
        return Response({"error": "list not found"}, status=404)

    todos = ToDoItems.objects.filter(list_name=todo_list)
    serializer = todoList_items_serializer(todos, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def add_todo_view(request):
    user = request.user
    list_name = request.data.get("todo_list_name")
    item_name = request.data.get("item_name")

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=list_name)
    except ToDoList.DoesNotExist:
        return Response({"error": "list not found"}, status=404)

    if ToDoItems.objects.filter(list_name=todo_list, item_name=item_name).exists():
        return Response({"error": "todo already exists"}, status=400)

    todo = ToDoItems.objects.create(
        list_name=todo_list,
        item_name=item_name,
        finished=False
    )

    return Response({
        "status": "created",
        "item": item_name
    })

@api_view(['DELETE'])
def delete_todo_view(request):
    user = request.user
    list_name = request.data.get("todo_list_name")
    item_name = request.data.get("item_name")

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=list_name)
    except ToDoList.DoesNotExist:
        return Response({"error": "list not found"}, status=404)

    todo_qs = ToDoItems.objects.filter(list_name=todo_list, item_name=item_name)

    if not todo_qs.exists():
        return Response({"error": "no such todo"}, status=404)

    todo_qs.delete()

    return Response({
        "status": "deleted",
        "item": item_name
    })

@api_view(['PATCH'])
def update_todo_view(request):
    user = request.user
    list_name = request.data.get("todo_list_name")
    item_name = request.data.get("item_name")

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=list_name)
    except ToDoList.DoesNotExist:
        return Response({"error": "list not found"}, status=404)

    try:
        todo = ToDoItems.objects.get(list_name=todo_list, item_name=item_name)
    except ToDoItems.DoesNotExist:
        return Response({"error": "no such todo"}, status=404)

    todo.finished = True
    todo.save()

    return Response({
        "status": "updated",
        "item": item_name,
        "finished": True
    })
