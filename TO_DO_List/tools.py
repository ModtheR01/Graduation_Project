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


