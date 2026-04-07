from agent import intent_chain


def run(user_message):
    # 1) نفهم
    action = intent_chain.invoke(user_message)

    # 2) لو دردشة
    if action.intent == "chat":
        return "Hello 👋"

    # 3) لو طيران
    if action.intent == "search_flights":
        if not action.origin:
            return "From where?"
        if not action.destination:
            return "To where?"
        if not action.date:
            return "Which date?"

        return agent.invoke({
            "origin": action.origin,
            "destination": action.destination,
            "date": action.date
        })
