from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from .AI_models import default_model
from .api_keys import OPENROUTER_KEY
from .prompt import system_prompt
from flights.views import booking_flight, search_flights
#from sending_emails.tools import search_in_contact, add_new_contact, send_email
#print(create_agent)
llm = ChatOpenAI(
    model=default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature=0.4,
)
#  , search_in_contact, add_new_contact, send_email
tools = [search_flights,booking_flight]
agent = create_agent(llm, tools=tools)
print("agent created ....")
def message_agent(chat_messages):
    messages = {"messages": [("system", system_prompt)]}
    for msg in chat_messages:
        messages["messages"].append((msg["role"], msg["content"]))
    response = agent.invoke(messages)["messages"][-1].content
    return response if response else "Sorry, I am a bit confused. Can you rephrase?"
