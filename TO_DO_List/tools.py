# no need to recreate agent as we will be using a single agent in the Core agent file for now 
from langchain_core.tools import tool
from .models import ToDoList
from .models import ToDoItems
from flights.state_store import get_store
from .serializers import todoList_items_serializer , todoList_serializer


# @tool
# def get_all_todo_items():
#     """
#     you can use this tool to return all todos available for the user
#     you can call this tool twice if the user gave you `todo_list_name` just to make sure it matches in the db 
#      1 --> so the first call will be to get all todo lists names from the database and identify which one the user propably want
#      2 --> the second call is to actually get the todos inside it by passing todo_list_name to the function

#     if the user provided a todolist name that isnt found in the database nor is simillar to another list name tell him that there is no such a list 

#     this funtion return list to todolists or list of todo items depending on which scenario

#     use this tool whenever the user ask about thier list
#     (e.g. what tasks should i do today )
#     (e.g. whats on my todo list today )
#     (e.g. what the remaining todos? )
#     (e.g. - show me all tasks / todos )
#     (e.g. what is the remaining tasks in my todo list )

#     """
#     store = get_store()
#     user_email = store.get("user_id") # id == email so mf34 fr2 
#     todo_lists = ToDoList.objects.filter(user_email = user_email)
#     if todo_list_name is not None:
#         todo_list = todo_lists.filter(list_name=todo_list_name).first()
#         if todo_list:
#             todo_items = ToDoItems.objects.filter(list_name= todo_list_name)
#             serialized_items = todoList_items_serializer(todo_items)
#             return serialized_items.data
#         else :
#             return "no such a list"
#     serialized_todo_lists = todoList_serializer(todo_lists)

#     return serialized_todo_lists.data


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

# @tool 
# def manage_todo(operation:int, todo_list_name:str , item_name:str):
#     """
#     you can use this tool to manage a todo in a specified `todo_list_name`
#     you can add new , delete , update status of a todo item in using this tool
#     parameters:
#     todo_list_name --> the name of the list the user want to add the todo in it 
#     item_name --> the name of the todo items (ex. study chapter 1)
#     operation --> this is a value you send depending on what operation you want to do (add,delete ,update):
#     -  `1` for adding a new todo item
#     -  `2` for deleting an already existing todo item
#     -  `3` for updating an already existing todo item
#     """
#     store = get_store()
#     user = store.get("user_id")

#     try:
#         todo_list = ToDoList.objects.get(user=user, list_name=todo_list_name)
#         todos = ToDoItems.objects.filter(list_name=todo_list)
#         todo = todos.get(item_name = item_name)
#     except ToDoList.DoesNotExist:
#         return "list not found"


#     if operation == 1:
#         print("will be adding in list :", todo_list_name)
#         if not todo:
#             todo = ToDoItems(
#                 list_name = todo_list,
#                 item_name = item_name,
#                 finished = False
#             )
#             todo.save()
#             print("new todo saved successfully :" , todo)
#         else:
#             print("already existing")
#             return "todo alraady existing"
#         return todo
    
#     if operation == 2:
#         if not todo:
#             print("no such todo")
#             return "no such todo"
#         todo.delete()

#     if operation == 3:
#         todo.finished = True
    
#     else:
#         print("sent wrong operation number:",operation)
#         return "please send a valid operation number"



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
