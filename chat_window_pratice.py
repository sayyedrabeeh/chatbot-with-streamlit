import streamlit as st

st.title('chat window')
with st.chat_message('assistant'):
    st.markdown('hi ,how are u ')
 

messages = st.chat_input('write your  input')
if messages :
    with st.chat_message('human'):
        st.markdown(messages)