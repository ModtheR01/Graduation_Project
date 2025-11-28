from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from Config.models_config import classify_model,default_model
from Config.settings import OPENROUTER_KEY
from Core.prompt import system_prompt
from Core.email_sending.tools import send_email, search_in_contact ,add_new_contact

llm = ChatOpenAI(
    model = default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
)

# TODO adding the rest of the tools
agent = create_agent(llm,[send_email, search_in_contact ,add_new_contact])
print("agent created ....")
messages = {"messages":[("system", system_prompt)]}

def message_agent(prompt):
    messages["messages"].append(("human", prompt))

    response = agent.invoke(messages)["messages"][-1].content
    print("assistant:", response)

    messages["messages"].append(( "ai",response))