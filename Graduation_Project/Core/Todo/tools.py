# no need to recreate agent as we will be using a single agent in the Core agent file for now 
from langchain_core.tools import tool
from Core.Todo.mock_todo import todo_list

@tool
def get_all_todo_items():
    """
    tool that return all tasks(todo items) use it when the user ask about his todo list or tasks he need to do
   
    it will return list of dictionaries of the todos available so you can show it to user

    use this tool whenever the user ask about thier list
    (e.g. what tasks should i do today )
    (e.g. whats on my todo list today )
    (e.g. what the remaining todos? )
    (e.g. - show me all tasks / todos )
    """
    return todo_list

@tool
def create_todo(name , status: False):
    # 7war en e7na nrg3 el list kolha da hyt4al lama el database tthat we hyb2a byt3rd fe saf7th bs
    """
    this tool is used to add a new todo item to the user todo list 

    the parameters are :
    name --> the name or the description of the todo item (e.g. clean my room)
    status --> a boolen value that indicate if the todo has been done or not by default its false unless the user told you he already done it and just wna to track it 

    it return the full list so you can send it to user to review it
    use this tool whenever the user want to add a todo item 
    (e.g. add a task of cleaning my room )
    (e.g. create a todo of finishing the lesson)
    """
    item = {
        "name":name,
        "is_done":status
    }
    todo_list.append(item)
    return todo_list

@tool 
def delete_todo(name):
    """
    this tool is used to delete todo item from the user todo list 
    when you are going to delete a task first call the get all list tool so you can provide the correct specific name the todo item is stored in the dataase with

    parameters:
    name --> the name or the description of the todo item (e.g. clean my room)

    return the updated list so you can send it to user to review it 

    use this tool whenever the user want to delete a todo item :
    (e.g. delete the task of cleaning my room )
    (e.g. delete the todo of finishing the lesson)

    """
    for todo in todo_list:
        if todo["name"] == name:
            todo_list.remove(todo)
            break
    return todo_list

@tool 
def set_state_true(name):
    """
    use this tool whenever the user want to set a specific todo item status to done (true)

    parameters:
    name --> the name or the description of the todo item (e.g. clean my room)

    return the updated list so you can send it to user to review it 

    use this tool whenever the user want to check a todo item 
    (e.g. i have done the task of cleaning my room )
    (e.g. set status of the todo of finishing the lesson to true)

    """
    for todo in todo_list:
        if todo["name"] == name:
            todo["is_done"] = True
    return todo_list