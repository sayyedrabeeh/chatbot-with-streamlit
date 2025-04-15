
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv() 
client = OpenAI()

def get_responses_from_llm(messages):
   completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

   return completion.choices[0].message.content

initial_messages=[
        { "role": "system",
            "content": ''' you are a trip planner in dubai . you are an expert in dubai tourism locations food events ,
                       hotels etc  you are able to guide users to plan"
                       their vaccations to dubat you should response proffesssionaly, your name dubai ginne short name DG 
                       always introduce  first with your name,response shouldn't exceed 200 words  always ask questions
                       help them to plan a trip finally give a daywise itnerary'''
        },
        {
            "role": "assistant",
            "content": "  your expert trip planner how can i help you  "
        }
    ]

if 'messages' not in st.session_state:
    st.session_state.messages=initial_messages
st.title('Dubai trip planner')
for messages in st.session_state.messages:
    if messages['role'] != 'system':
      with st.chat_message(messages['role']):
          st.markdown(messages['content'])

user_input = st.chat_input("Ask anything to Dubai GiNNee...")
if user_input:
    new_messagess= {
            "role": "user",
            "content": user_input
        }
    st.session_state.messages.append(new_messagess)
    with st.chat_message(new_messagess['role']):
            st.markdown(new_messagess['content'])
    response = get_responses_from_llm(st.session_state.messages)
    if response:
         response_messagess= {
            "role": "assistant",
            "content": response
        }
    st.session_state.messages.append(response_messagess)

    with st.chat_message(response_messagess['role']):
            st.markdown(response_messagess['content'])

