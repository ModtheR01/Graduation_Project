# from langchain.agents import create_react_agent
# from langchain_openai import ChatOpenAI
# from .AI_models import default_model
# from .api_keys import OPENROUTER_KEY
# from .prompt import system_prompt
# # from Core.search_flights.tools import search_for_flights
# # from Core.Flights.tools import flight_order
# # from Core.email_sending.tools import send_email, search_in_contact ,add_new_contact
# # from Core.Todo.tools import create_todo,delete_todo,set_state_true,get_all_todo_items

# llm = ChatOpenAI(
#     model = default_model,
#     api_key=OPENROUTER_KEY,
#     base_url="https://openrouter.ai/api/v1",
#     streaming=False,
#     temperature =0.2,
# )
# #[send_email, search_in_contact ,add_new_contact,create_todo,delete_todo,set_state_true,get_all_todo_items,search_for_flights,flight_order]
# # TODO adding the rest of the tools
# agent = create_react_agent(llm, tools=[],prompt=system_prompt)
# #agent = create_agent(llm,[search_for_flights])
# print("agent created ....")

# def message_agent(chat_messages):
#     messages = {"messages": []}

#     for msg in chat_messages: # receive all chat and loop on it to be understandable to the agent
#         messages["messages"].append(
#             (msg["role"], msg["content"])
#         )

#     response = agent.invoke(messages)["messages"][-1].content

#     if response != "":
#         return response
#     else:
#         return "Sorry, I am a bit confused. Can you rephrase?"
    

# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from .AI_models import default_model
# from .api_keys import OPENROUTER_KEY
# from .prompt import system_prompt

# llm = ChatOpenAI(
#     model=default_model,
#     api_key=OPENROUTER_KEY,
#     base_url="https://openrouter.ai/api/v1",
#     streaming=False,
#     temperature=0.2,
# )

# print("agent created ....")

# def message_agent(chat_messages):
#     messages = [SystemMessage(content=system_prompt)]

#     for msg in chat_messages:
#         if msg["role"] == "human":
#             messages.append(HumanMessage(content=msg["content"]))
#         else:
#             messages.append(AIMessage(content=msg["content"]))

#     response = llm.invoke(messages)
#     return response.content if response.content else "Sorry, I am a bit confused. Can you rephrase?"





# from langchain_classic.agents import create_react_agent, AgentExecutor
# from langchain_classic.memory import ConversationBufferMemory
# from langchain_classic.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI
# from .AI_models import default_model
# from .api_keys import OPENROUTER_KEY
# from .prompt import system_prompt

# llm = ChatOpenAI(
#     model=default_model,
#     api_key=OPENROUTER_KEY,
#     base_url="https://openrouter.ai/api/v1",
#     streaming=False,
#     temperature=0.2,
# )

# prompt_template = PromptTemplate.from_template(
#     system_prompt + """

# Tools available:
# {tools}

# Tool names: {tool_names}

# Chat History:
# {chat_history}

# User: {input}

# {agent_scratchpad}"""
# )

# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=False
# )

# agent = create_react_agent(llm=llm, tools=[], prompt=prompt_template)

# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[],
#     memory=memory,
#     handle_parsing_errors=True,
#     verbose=True
# )

# print("agent created ....")

# def message_agent(chat_messages):
#     try:
#         last_message = chat_messages[-1]["content"]
#         response = agent_executor.invoke({"input": last_message})["output"]
#         return response if response else "Sorry, I am a bit confused. Can you rephrase?"
#     except Exception as e:
#         print(f"Agent error: {e}")
#         return "Sorry, I am a bit busy right now. Please try again!"


from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from .AI_models import default_model
from .api_keys import OPENROUTER_KEY
from .prompt import system_prompt
# from Core.search_flights.tools import search_for_flights
# from Core.Flights.tools import flight_order
# from Core.email_sending.tools import send_email, search_in_contact, add_new_contact
# from Core.Todo.tools import create_todo, delete_todo, set_state_true, get_all_todo_items

llm = ChatOpenAI(
    model=default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature=0.2,
)

tools = []


agent = create_agent(llm, tools=tools)
print("agent created ....")

def message_agent(chat_messages):
    messages = {"messages": [("system", system_prompt)]}

    for msg in chat_messages:
        messages["messages"].append((msg["role"], msg["content"]))

    response = agent.invoke(messages)["messages"][-1].content

    return response if response else "Sorry, I am a bit confused. Can you rephrase?"









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
# def message_agent(prompt):
#     messages["messages"].append(("human", prompt))
#     response = agent.invoke(messages)["messages"][-1].content

#     if response != "":
#         final_response = response
#     else:
#         final_response = "Sorry, I am a bit confused. Can you rephrase?"

#     messages["messages"].append(("ai", final_response))

#     return final_response

