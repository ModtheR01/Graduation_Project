from langchain.agents import create_agent
from Core.email_sending.tools import send_email,search_in_contact,add_new_contact
from langchain_openai import ChatOpenAI
from Config.models_config import default_model
from Config.settings import OPENROUTER_KEY
from Core.email_sending.prompt import system_prompt,human_prompt,assistant_prompt
from langchain_core.prompts import PromptTemplate


#what_To_Send=PromptTemplate("before sending tis email take user approval :{send_mail}")
#is_Approved = PromptTemplate.from_template("yes i approve on {mail}")

# another model created here to test if there is a model better than another in email sending specific task
# if we will use the same model it will be created once and imported 

llm = ChatOpenAI(
    model = default_model,
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.5, # need it to be a bit creative since we will be writing mails
    #max_tokens=4096,
    streaming=False, # send the response while being generated set to flase since its dealing with tool
)

agent = create_agent(
    llm,
    tools=[send_email,search_in_contact,add_new_contact],              
)

print("Agent Created...")
result = agent.invoke({
    "messages":[("system",system_prompt)
                #,("ai",assistant_prompt)
                ,("human",human_prompt)]
})
print(result["messages"][-1].content)

#the proplem i was facing here is that i cant send one prompt and the model come back looking for confirmation
# so i needed a way to check for approval or we will need to send the mail through code not model
# i added is approved to force the model check back with the user before sending the email 
# for it to work we need to implement chat memory so the model see that the mail has been written before 
# and it was approved by user to be sent i mimicked it by using assistant prompt


# we also need to give the model some user info by RAG so it can use it e.g. in the sending email 
# setting the username automaticaly without asking the user for his name 

