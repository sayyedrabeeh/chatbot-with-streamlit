import streamlit as st 

st.title('hello from Upcode')

name = st.text_input('enter your name :')

if st.button('hello '):
    st.write(f'hello {name} welcome to upcode ')