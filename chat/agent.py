from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from .AI_models import default_model
from .api_keys import OPENROUTER_KEY
from .prompt import system_prompt
from flights.views import booking_flight, search_flights
#from sending_emails.tools import search_in_contact, add_new_contact, send_email
from flights.views import search_flights
from sending_emails.tools import search_in_contact, add_new_contact, send_email
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
#  , search_in_contact, add_new_contact, send_email
tools = [search_flights,booking_flight, send_email]
#tools = [search_flights,send_email] 
agent = create_agent(llm, tools=tools,max_iterations=1)
print("agent created ....")
def message_agent(user_id,chat_messages):
    print("in message_agent Step2 : the view is working fine" )
    messages = {"user_id":user_id,"messages": [("system", system_prompt)]}
    print("user_id :",user_id ,"type :", type(user_id))
    for msg in chat_messages:
        messages["messages"].append((msg["role"], msg["content"]))
    response = agent.invoke(messages)["messages"][-1].content
    return response if response else "Sorry, I am a bit confused. Can you rephrase?"
