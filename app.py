import streamlit as st
import requests
import re

# Backend API URL
API_URL = "http://127.0.0.1:8000/get_weather"

st.set_page_config(page_title="Weather Bot 🌦️", page_icon="🌍")
st.title("🌦️ Weather Bot")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to categorize query
def categorize_query(query: str) -> str:
    if query.isdigit():
        return "postal code"
    elif re.search(r"\d{5,6}", query):  # Indian or US zip-like patterns
        return "postal code"
    elif re.search(r"[,]", query):  # If contains comma, likely city+country
        return "city"
    elif len(query.split()) <= 2:
        return "city"
    else:
        return "landmark / general location"

# Chat input box (Streamlit’s chat UI)
if user_query := st.chat_input("Ask about the weather..."):
    # Append user query
    category = categorize_query(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query, "category": category})

    # Fetch from backend
    try:
        response = requests.post(API_URL, json={"query": user_query})
        if response.status_code == 200:
            answer = response.json().get("answer", "No response")
        else:
            answer = f"❌ Error: {response.status_code}"
    except Exception as e:
        answer = f"⚠️ Backend not reachable: {e}"

    # Append bot response
    st.session_state.messages.append({"role": "bot", "content": answer})

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(f"🧑‍💻 {msg['content']}")
            st.caption(f"Detected type: **{msg.get('category', 'unknown')}**")
    else:
        with st.chat_message("assistant"):
            st.write(f"🤖 {msg['content']}")
