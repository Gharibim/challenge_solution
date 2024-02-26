import streamlit as st
from streamlit_chat import message
import json
import os 

from llm import gpt_request
from conversation import take_action

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'update_counter' not in st.session_state:
    st.session_state['update_counter'] = 0

st.set_page_config(page_title="Chat GPT Clone", page_icon=":robot_face:")

st.markdown("<h1 style='text-align: center;'>Upload a conversation to start</h1>", unsafe_allow_html=True)

st.sidebar.title("Configuration")
st.session_state['API_Key'] = OPENAI_API_KEY

uploaded_file = st.sidebar.file_uploader("Upload a JSON file", type=['json'])

if 'conversation_display' not in st.session_state:
    st.session_state['conversation_display'] = st.empty()

def display_conversation_from_json(json_data):
    update_counter = st.session_state['update_counter']
    st.session_state['conversation_display'].empty()
    new_display = st.empty()
    with new_display.container():
        for i, entry in enumerate(json_data):
            key = f"msg_{i}_{entry['id']}_{update_counter}"
            is_user = entry['role'] == 'user'
            message(entry['content'], is_user=is_user, key=key)
    st.session_state['conversation_display'] = new_display

if uploaded_file is not None:
    json_data = json.load(uploaded_file)
    st.session_state['conversation'] = json_data
    st.session_state['update_counter'] = 0
    display_conversation_from_json(json_data)

user_input = st.text_area("Enter an action:", height=100)
send_button = st.button(label='Send')

if send_button and user_input:
    action = gpt_request(st.session_state['conversation'], user_input)
    updated_conversation_json = take_action(st.session_state['conversation'], action)
    st.session_state['conversation'] = updated_conversation_json
    st.session_state['update_counter'] += 1
    display_conversation_from_json(updated_conversation_json)

