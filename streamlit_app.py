import streamlit as st

st.set_page_config(page_title="My App", layout="centered")

st.title("Hello, Streamlit! 👋")
st.subheader("This is a quick demo page.")

name = st.text_input("Enter your name:")
if name:
    st.success(f"Hi {name}! Welcome to Streamlit.")
    
number = st.slider("Pick a number", 0, 100)
st.write(f"You selected: {number}")
