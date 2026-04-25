# no need to recreate agent as we will be using a single agent in the Core agent file for now 
from langchain_core.tools import tool
from .models import ToDoList
from .models import ToDoItems
from flights.state_store import get_store
from .serializers import todoList_items_serializer , todoList_serializer




@tool
def get_all_todo_lists():
    """
    you can use this tool to return all todo lists available for the user
    so whenever the user asks for his tasks or his todos in general or his lists you will be calling this tool
    """
    store = get_store()
    user = store.get("user_id") # id == email so mf34 fr2 
    todo_lists = ToDoList.objects.filter(user = user)

    serialized_todo_lists = todoList_serializer(todo_lists, many=True)

    return serialized_todo_lists.data

@tool 
def get_items_inList(todo_list_name: str):
    """
    use this tool to get all tasks inside a single list you should provide the name correctly as its stored in the database
    it return list of todo items in a specified list
    """
    store = get_store()
    user = store.get("user_id")

    if not todo_list_name:
        return "please provide a todo list name"

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=todo_list_name)
    except ToDoList.DoesNotExist:
        return "list not found"

    todos = ToDoItems.objects.filter(list_name=todo_list)

    serialized_todos = todoList_items_serializer(todos, many=True)

    return serialized_todos.data

@tool 
def manage_todo(operation: int, todo_list_name: str, item_name: str):
    """
    you can use this tool to manage a todo in a specified `todo_list_name`
    you can add new , delete , update status of a todo item in using this tool
    parameters:
    todo_list_name --> the name of the list the user want to add the todo in it 
    item_name --> the name of the todo items (ex. study chapter 1)
    operation --> this is a value you send depending on what operation you want to do (add,delete ,update):
    -  `1` for adding a new todo item
    -  `2` for deleting an already existing todo item
    -  `3` for updating an already existing todo item
    """
    store = get_store()
    user = store.get("user_id")

    try:
        todo_list = ToDoList.objects.get(user=user, list_name=todo_list_name)
    except ToDoList.DoesNotExist:
        return "list not found"

    todo_qs = ToDoItems.objects.filter(list_name=todo_list, item_name=item_name)

    # 🔹 ADD
    if operation == 1:
        if todo_qs.exists():
            return "todo already exists"

        todo = ToDoItems.objects.create(
            list_name=todo_list,
            item_name=item_name,
            finished=False
        )

        return {
            "status": "created",
            "item": item_name
        }

    # 🔹 DELETE
    elif operation == 2:
        if not todo_qs.exists():
            return "no such todo"

        todo_qs.delete()
        return {
            "status": "deleted",
            "item": item_name
        }

    # 🔹 UPDATE
    elif operation == 3:
        if not todo_qs.exists():
            return "no such todo"

        todo = todo_qs.first()
        todo.finished = True
        todo.save()

        return {
            "status": "updated",
            "item": item_name,
            "finished": True
        }

    # 🔹 INVALID OPERATION
    else:
        return "please send a valid operation number"
