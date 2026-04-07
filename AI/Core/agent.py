from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from Config.models_config import default_model
from Config.settings import OPENROUTER_KEY
from Core.prompt import system_prompt
from Core.search_flights.tools import search_for_flights
from Core.Flights.tools import flight_order
#from Core.search_flights.s import AgentAction
from Core.email_sending.tools import send_email, search_in_contact ,add_new_contact
from Core.Todo.tools import create_todo,delete_todo,set_state_true,get_all_todo_items
#from Core.Flights.tools import *

llm = ChatOpenAI(
    model = default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature =0.2,
)

# TODO adding the rest of the tools
agent = create_agent(llm,[send_email, search_in_contact ,add_new_contact,create_todo,delete_todo,set_state_true,get_all_todo_items,search_for_flights,flight_order])
#agent = create_agent(llm,[search_for_flights])
print("agent created ....")
messages = {"messages":[("system", system_prompt)]}

# def message_agent(prompt):
#     messages["messages"].append(("human", prompt))
#     response = agent.invoke(messages)["messages"][-1].content
#     #response = agent.invoke(messages)
#     if response != "":
#         print("assistant:", response)
#     else:
#         print("assistant:", "Sorry, i am a bit confused can you please ask me again in more simple way")
#     messages["messages"].append(( "ai",response))


# now we use it because streamlit deal with return not print
def message_agent(prompt):
    messages["messages"].append(("human", prompt))
    response = agent.invoke(messages)["messages"][-1].content

    if response != "":
        final_response = response
    else:
        final_response = "Sorry, I am a bit confused. Can you rephrase?"

    messages["messages"].append(("ai", final_response))

    return final_response
