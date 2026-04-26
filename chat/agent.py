from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from .AI_models import default_model
from .api_keys import OPENROUTER_KEY
from .prompt import system_prompt
from flights.views import booking_flight, search_flights
#from sending_emails.tools import search_in_contact, add_new_contact, send_email
from flights.views import search_flights
from sending_emails.tools import search_in_contact, add_new_contact, send_email ,delete_contact
from Hotels.views import search_hotels,booking_hotel
from TO_DO_List.tools import get_all_todo_lists, get_items_inList ,manage_todo ,create_list, delete_list
#print(create_agent)
llm = ChatOpenAI(
    model=default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature=0.4,
    model_kwargs={
        "parallel_tool_calls": False  # ✅ امنع الـ parallel calls
    }
)
#  all tools added now except for reminder
tools = [search_flights,booking_flight,delete_contact, send_email,search_hotels,booking_hotel,get_all_todo_lists,get_items_inList,manage_todo,search_in_contact, add_new_contact,create_list,delete_list]
#tools = [search_flights,send_email] 
agent = create_agent(llm, tools=tools)
print("agent created ....")

def message_agent(chat_messages):
    print("in message_agent Step2" )

    messages = {"messages": [("system", system_prompt)]}
    for msg in chat_messages:
        messages["messages"].append((msg["role"], msg["content"]))

    response = agent.invoke(
        messages,
        config={
            "recursion_limit": 25   # يسمح بـ multiple tool calls
        })
    
    return response["messages"][-1].content if response else "Sorry, I am a bit confused. Can you rephrase?"
