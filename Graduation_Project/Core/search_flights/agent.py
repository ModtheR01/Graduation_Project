{
# # Core/agent_create_v1.py
# from langchain_classic.agents import AgentExecutor
# from Core.tools import dispalyed_flighs
# from Config.models_config import default_model
# from Config.settings import OPENROUTER_KEY
# from langchain_core.prompts import PromptTemplate
# from langchain_classic import hub
# from langchain_openai import ChatOpenAI        
# from langchain.agents import create_agent
# from langchain_classic.agents import initialize_agent, AgentType


# # ← الحل السحري (سطرين بس)
# llm = ChatOpenAI(
#     model=default_model,                     # مثلاً: "deepseek/deepseek-chat"
#     api_key=OPENROUTER_KEY,                  # مفتاحك من OpenRouter
#     base_url="https://openrouter.ai/api/v1", # ده اللي بيخلّيه يروح لـ OpenRouter
#     temperature=0,
#     max_tokens=4096,                         # اختياري، حسب الموديل
# )
# # اختبار سريع
# #print(llm.invoke("Hi").content)
# #----------------------------------------------------------------------
# prompt = hub.pull("hwchase17/react")
# template="explain the concept:{concept}"
# pt=PromptTemplate.from_template(template=template)
# # prompt=pt.invoke({"concept":"Prompting LLMS"})
# # print(prompt)
# chain= pt | llm
# concept="American Football"
# # print(chain.invoke({"concept":concept}))
# agent = initialize_agent(
#     tools=[dispalyed_flighs],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     handle_parsing_errors=True,
# )

# # message=agent.invoke({"message":[("human","search for flights")]})
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[dispalyed_flighs],
#     verbose=True,                      # عشان تشوف التفكير خطوة بخطوة
#     handle_parsing_errors=True,
#     max_iterations=15,
# )
# response = agent.invoke({
#     "input": "search for flights"
# })
# print(response["output"])


# # # --- tools: use your @tool decorated function directly ---
# # tools = [dispalyed_flighs]

# # # --- create the agent (langchain v1 style) ---
# # agent = create_agent(
# #     model=llm,                      # pass the LLM instance
# #     tools=tools,
# #     system_prompt="You are an agent that must call tools to find flight offers. Use the 'search_flights' tool with origin, destination, date.",
# # )

# # # --- flexible invocation helper (some v1 objects use invoke, others run) ---
# # def run_agent_query(agent_obj, query: str):
# #     # prefer invoke({"input": ...}) (v1-style)
# #     if hasattr(agent_obj, "invoke") and callable(agent_obj.invoke):
# #         out = agent_obj.invoke({"input": query})
# #         # often returns dict with "output"
# #         if isinstance(out, dict) and "output" in out:
# #             return out["output"]
# #         return out
# #     # fallback to run(query)
# #     if hasattr(agent_obj, "run") and callable(agent_obj.run):
# #         return agent_obj.run(query)
# #     # last resort: call the agent object
# #     if callable(agent_obj):
# #         return agent_obj(query)
# #     raise RuntimeError("Can't invoke agent with known patterns")

# # if __name__ == "__main__":
# #     q = "Find cheapest flights from CAI to DXB on 2026-11-10"
# #     print("Query:", q)
# #     res = run_agent_query(agent, q)
# #     print("\n=== AGENT RESULT ===\n")
# #     # pretty print if dict
# #     if isinstance(res, dict):
# #         print(json.dumps(res, indent=2, ensure_ascii=False))
# #     else:
# #         print(res)
}
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from Graduation_Project.Core.search_flights.tools import search_for_flights
from Config.settings import OPENROUTER_KEY , GEMINI_KEY
from Config.models_config import default_model

# ✅ استخدم Llama 3.1 بدل DeepSeek (مجاني وبيدعم Tools)
llm = ChatOpenAI(
    model=default_model,  
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=4096,
    streaming=False,
)
# اختبار
print("🔄 Testing LLM...")
test_response = llm.invoke("Say 'Hello, I am ready!'")
print(test_response.content)
print("\n✅ LLM is working!\n")

# 🚀 إنشاء Agent
print("🤖 Creating agent...")
agent = create_agent(llm, tools=[search_for_flights])

# تشغيل
print("✈️ Searching for flights...\n")
result = agent.invoke({
    "messages": [("system", "You are a helpful travel assistant. Always return clean JSON flight results with prices and departure times. also make sure the date is in this format YEAR-Month-DAY"),
                 ("user", "search for flights from new york city to singapore in 27 november 2025")]
})

# النتيجة
print("\n📋 Final Result:")
print(result["messages"][-1].content)