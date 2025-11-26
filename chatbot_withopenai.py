import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

 
load_dotenv()
 
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

 
model = genai.GenerativeModel("gemini-1.5-flash")

def get_responses_from_llm(messages):
    
    history = []
    for m in messages:
        history.append({"role": m["role"], "parts": [m["content"]]})

    response = model.generate_content(history)
    return response.text

 

initial_messages = [
    {
        "role": "system",
        "content": """you are a trip planner in dubai . you are an expert 
        in dubai tourism locations food events, hotels etc. You guide users 
        to plan their vacations professionally. Your name is Dubai Ginnee (DG). 
        Always introduce first with your name, respond within 200 words, always 
        ask follow-up questions and give a day-wise itinerary."""
    },
    {
        "role": "assistant",
        "content": "I am Dubai Ginnee (DG), your expert trip planner. How can I help you?"
    }
]

if 'messages' not in st.session_state:
    st.session_state.messages = initial_messages

st.title("Dubai Trip Planner (DG)")

 
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
 
user_input = st.chat_input("Ask anything to Dubai Ginnee...")

if user_input:
    new_user_msg = {"role": "user", "content": user_input}
    st.session_state.messages.append(new_user_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    response = get_responses_from_llm(st.session_state.messages)

    assistant_msg = {"role": "assistant", "content": response}
    st.session_state.messages.append(assistant_msg)

    with st.chat_message("assistant"):
        st.markdown(response)
