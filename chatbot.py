import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load DistilGPT-2 model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    return tokenizer, model

tokenizer, model = load_model()

# Chat header
st.set_page_config(page_title="Dubai GiNNee", layout="centered")
st.title("🧞 Dubai GiNNee - Your Dubai Trip Planner")
st.markdown("Ask me anything about your Dubai trip! ✈️🕌🌆")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to generate a reply
def generate_reply(history, user_input):
    prompt = "You are Dubai GiNNee, a helpful and concise AI travel planner for Dubai.\n"
    for msg in history:
        prompt += f"User: {msg['user']}\nDubai GiNNee: {msg['assistant']}\n"
    prompt += f"User: {user_input}\nDubai GiNNee:"

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=inputs["input_ids"].shape[1] + 100,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
    )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply = generated_text.split("Dubai GiNNee:")[-1].strip()
    return reply

# Chat UI
user_input = st.chat_input("Ask Dubai GiNNee anything...")

if user_input:
    # Generate response
    reply = generate_reply(st.session_state.chat_history, user_input)

    # Save in session
    st.session_state.chat_history.append({
        "user": user_input,
        "assistant": reply
    })

# Display chat
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(f"🤖 Dubai GiNNee: {chat['assistant']}")

