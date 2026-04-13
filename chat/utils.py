from langchain_openai import ChatOpenAI

title_model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key='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',
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature=0.4,
)

def generate_title(user_message):
    messages = [
        ("system", system_prompt),
        ("human", user_message),
    ]
    print("Generating title for message:", user_message)
    response = title_model.invoke(messages).content.strip()
    print("Generated title:", response)

    return response if response else "New Chat"

models_list=["google/gemma-4-31b-it:free","google/gemma-4-26b-a4b-it:free","nvidia/nemotron-3-super-120b-a12b:free"]

system_prompt = (
                    """
                RULES:
                - YOU CAN GENERATE ONLY ONE TITLE PER REQUEST ONLY ONE!
                - Generate a short, natural-sounding chat title (max 8 words).
                - if you got a inappropriate content generate a title that indicates that without being explicit like "inappropriate content" or "content not allowed" 
                - dont ever generate an empty title or a message to user title as there will be no one to read it it will be directly stored in the db so you need to work your way around it
                - make sure the title is in the same language the user used 
                
                The title should:
                - sound like a real conversation topic
                - summarize the main intent only
                - ignore extra details like dates unless very important
                - be clean and readable

                Bad example:
                "book flight cairo paris december 20 suggestions paris sites"
                "email create contact john details"

                Good examples:
                "Trip to Paris Planning"
                "Flight and Paris Travel Ideas"
                "new contact creation for john"
                """
            ),
