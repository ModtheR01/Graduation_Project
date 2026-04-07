from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from Graduation_Project.Core.search_flights.tools import search_for_flights
from Config.settings import OPENROUTER_KEY , GEMINI_KEY
from Config.models_config import default_model

llm = ChatOpenAI(
    model=default_model,  
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=4096,
    streaming=False,
)

print("🔄 Testing LLM...")
test_response = llm.invoke("Say 'Hello, I am ready!'")
print(test_response.content)
print("\n✅ LLM is working!\n")


print("🤖 Creating agent...")
agent = create_agent(llm, tools=[search_for_flights])


print("✈️ Searching for flights...\n")
result = agent.invoke({
    "messages": [("system", "you are an assistant take actions by using user's prompt, donot take actions without using one or more of the tools")],
    "messages": [("user", "i want flights from Cairo to Dubai in 2025-11-27")],

})


# print("\n📋 Final Result:")
# print(result["messages"][-1].content)