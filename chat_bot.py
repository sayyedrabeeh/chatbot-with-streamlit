import streamlit as st
import requests
import json


st.title("🧞 Dubai Ginnee - Your Dubai Trip Planner")
st.markdown("Ask me anything about your Dubai trip! ✈️🕌")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

 
def generate_reply(history, user_input):
     
    full_prompt = ""
    for msg in history:
        full_prompt += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n"
    full_prompt += (
        f"User: {user_input}\n"
        "Assistant (reply within 100 words, keep it efficient  and clear you are a dubaii trip planner ):"
    )
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": full_prompt,
                "stream": True,
                "temperature": 0.7,
                "top_p": 0.95,
                "stop": ["User:", "Assistant:"]
            },
            stream=True
        )
        
        reply = ""
        
   
        
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    chunk = data.get("response", "")
                    reply += chunk
                    if len(reply.split()) > 100:
                        reply = " ".join(reply.split()[:100]) + "..."
                        break
                except json.JSONDecodeError:
                    continue
        
        return reply.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

 
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(f"🤖 Dubai GiNNee: {chat['assistant']}")

 
user_input = st.chat_input("Ask anything to Dubai GiNNee...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Dubai Ginnee is thinking..."):
            reply = generate_reply(st.session_state.chat_history, user_input)
            st.markdown(f"🤖 Dubai ginnee: {reply}")
    
 
    st.session_state.chat_history.append({"user": user_input, "assistant": reply})