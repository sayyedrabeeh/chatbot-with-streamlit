import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
 
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

 
model = genai.GenerativeModel(
    "models/gemini-2.5-flash",
    system_instruction="""
You are Dubai Ginnee (DG), an expert Dubai trip planner.
You know all Dubai attractions, food spots, hotels, events, and transportation.
Your responses must:
- Start with a friendly DG introduction.
- Stay under 200 words.
- Include follow-up questions.
- Provide day-wise itinerary guidance.
"""
)

 
def get_responses_from_llm(messages):
    gemini_messages = []

    for m in messages:
        
        if m["role"] == "system":
            continue

      
        role = "model" if m["role"] == "assistant" else "user"

        gemini_messages.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })

    
    response = model.generate_content(gemini_messages)
    return response.text


 
st.title("Dubai Trip Planner (DG) 🕌✨")

 
initial_messages = [
    {
        "role": "assistant",
        "content": "I am Dubai Ginnee (DG), your expert trip planner! 🌴✨ How can I help you plan your perfect Dubai vacation?"
    }
]

 
if "messages" not in st.session_state:
    st.session_state.messages = initial_messages

 
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
