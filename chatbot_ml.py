import random

# Keywords and intents
intents = {
    "greetings": ["hi", "hello", "hey"],
    "goodbye": ["bye", "goodbye"],
    "how_are_you": ["how are you", "how r u"],
    "study_tip": ["study tip", "tips", "advice", "how to study"],
    "resources": ["resources", "links", "online", "books"],
    "time_management": ["time management", "plan", "schedule"]
}

responses = {
    "greetings": ["Hello! 😄 How can I help you study today?", "Hey there! Ready to learn?"],
    "goodbye": ["Bye 👋 Keep studying hard!", "See you! Stay focused 💪"],
    "how_are_you": ["I’m ready to help you study! How about you?", "I’m doing great! Let’s learn something new."],
    "study_tip": [
        "Break your study into 25-min focused sessions with 5-min breaks. 🍀",
        "Always revise what you learned in the same day. 📚"
    ],
    "resources": [
        "Check out free resources like Coursera, edX, and YouTube tutorials.",
        "For Python, try w3schools, GeeksforGeeks, or official documentation."
    ],
    "time_management": [
        "Make a weekly schedule and prioritize difficult topics first.",
        "Use a planner or Google Calendar to allocate study slots."
    ]
}

def chatbot_response(msg):
    msg = msg.lower()
    for intent, keywords in intents.items():
        for word in keywords:
            if word in msg:
                return random.choice(responses[intent])
    # Default fallback
    return "Hmm 🤔 I’m still learning about that. Can you try asking differently?"
