def get_bot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! How can I help you?"
    elif "project" in user_input:
        return "I can help you with software projects."
    elif "bye" in user_input:
        return "Goodbye! Have a great day."
    else:
        return "Sorry, I didn't understand that."
