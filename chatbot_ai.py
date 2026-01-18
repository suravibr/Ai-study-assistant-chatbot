import os
import json
import random
import PyPDF2
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from rapidfuzz import fuzz

# Load knowledge base
with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

# Casual intents
intents = {
    "greetings": ["hi", "hello", "hey"],
    "goodbye": ["bye", "goodbye"],
    "how_are_you": ["how are you", "how r u"]
}

casual_responses = {
    "greetings": ["Hello! 😄 How can I help you study today?", "Hey! Ready to learn?"],
    "goodbye": ["Bye 👋 Keep studying hard!", "See you! Stay focused 💪"],
    "how_are_you": ["I’m ready to help you study! How about you?", "I’m doing great! Let’s learn something new."]
}

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Store PDF chunks and embeddings
pdf_chunks = []
pdf_embeddings = []

# ----------------- PDF handling -----------------
def add_pdf_text(filepath):
    global pdf_chunks, pdf_embeddings
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Split into paragraphs
    chunks = [re.sub(r'\s+', ' ', p.strip()) for p in text.split("\n") if p.strip()]
    pdf_chunks.extend(chunks)

    # Compute embeddings
    embeddings = model.encode(chunks)
    if len(pdf_embeddings) == 0:
        pdf_embeddings = embeddings
    else:
        pdf_embeddings = np.vstack([pdf_embeddings, embeddings])

# ----------------- Chatbot response -----------------
def chatbot_response(msg):
    msg_clean = re.sub(r'\s+', ' ', msg.lower().strip())  # remove extra spaces

    # 1. Casual responses
    for intent, keywords in intents.items():
        for word in keywords:
            if fuzz.partial_ratio(word, msg_clean) > 80:  # tolerate typos
                return random.choice(casual_responses[intent])

    # 2. Knowledge base
    for key, answer in kb.items():
        if fuzz.partial_ratio(key.lower(), msg_clean) > 70:
            return answer

    # 3. PDF-based response
    if pdf_chunks:
        query_vec = model.encode([msg_clean])
        sims = cosine_similarity(query_vec, pdf_embeddings)[0]
        idx = np.argmax(sims)
        if sims[idx] > 0.5:  # similarity threshold
            return pdf_chunks[idx][:500]  # first 500 chars

    # 4. Fallback
    return ("I’m not sure about that..")
