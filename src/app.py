# File: openrouter-streamlit-chat/src/app.py

import os
import streamlit as st
from dotenv import load_dotenv

from api.openrouter_client import OpenRouterClient
from services.chat_service import ChatService
from models.message import Message

# Load .env file if present
load_dotenv()

st.set_page_config(page_title="OpenRouter Chat", page_icon="💬")
st.title("Chat Application with OpenRouter API")

def _secret_get(key: str):
    # Guarded access to st.secrets (it raises if no secrets.toml exists)
    try:
        return st.secrets.get(key)
    except Exception:
        return None

# Prefer environment/.env first, then optional secrets.toml
api_key = (
    os.getenv("OPENROUTER_API_KEY")
    or os.getenv("API_KEY")
    or _secret_get("OPENROUTER_API_KEY")
    or _secret_get("API_KEY")
)
model_id = (
    os.getenv("OPENROUTER_MODEL")
    or os.getenv("MODEL")
    or _secret_get("OPENROUTER_MODEL")
    or _secret_get("MODEL")
    or "openai/gpt-oss-120b" 
)
referer = (
    os.getenv("OPENROUTER_HTTP_REFERER")
    or os.getenv("HTTP_REFERER")
    or _secret_get("OPENROUTER_HTTP_REFERER")
    or _secret_get("HTTP_REFERER")
)
site_title = (
    os.getenv("OPENROUTER_SITE_TITLE")
    or os.getenv("SITE_TITLE")
    or _secret_get("OPENROUTER_SITE_TITLE")
    or _secret_get("SITE_TITLE")
)

if not api_key:
    st.error(
        "API key not found. Set API_KEY (or OPENROUTER_API_KEY) in your .env or environment.\n"
        'PowerShell example:  $env:API_KEY = "sk-or-..."'
    )
    st.stop()

# Initialize client/service once per session
if "chat_service" not in st.session_state:
    client = OpenRouterClient(
        api_key=api_key,
        model=model_id,
        referer=referer,
        site_title=site_title,
    )
    st.session_state.chat_service = ChatService(client)
    st.session_state.messages = []

chat_service: ChatService = st.session_state.chat_service

# Sidebar info 
with st.sidebar:
    st.caption("Model")
    st.code(model_id, language=None)
    st.caption("Base URL")
    st.code("https://openrouter.ai/api/v1", language=None)

# Chat history UI
for m in st.session_state.messages:
    if m.sender.lower() == "user":
        st.chat_message("user").markdown(m.content)
    else:
        st.chat_message("assistant").markdown(m.content)

# Input box
prompt = st.chat_input("Type your message...")

if prompt:
    user_msg = Message(content=prompt, sender="User")
    st.session_state.messages.append(user_msg)
    st.chat_message("user").markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            reply = chat_service.process_message(user_msg, history=st.session_state.messages[:-1])
        except Exception as e:
            st.error(f"Request failed: {e}\nTip: ensure MODEL=openai/gpt-oss-120b")
            st.stop()

    st.session_state.messages.append(reply)
    st.chat_message("assistant").markdown(reply.content)