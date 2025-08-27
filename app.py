import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/get_weather"

st.set_page_config(page_title="Weather Bot 🌦️", page_icon="🌍")
st.title("🌦️ Weather Bot")

query = st.text_input("Ask about the weather (city, zipcode, landmark...)", "")

if st.button("Get Weather"):
    if query.strip():
        with st.spinner("Fetching weather..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    answer = response.json().get("answer", "No response")
                    st.success(answer)
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Backend not reachable: {e}")
    else:
        st.warning("Please enter a query.")
