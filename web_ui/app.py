import streamlit as st
import requests

st.title("Chat Project Web UI")

if st.button("API 상태 확인"):
    resp = requests.get("http://api:8000/")
    st.write(resp.json()) 