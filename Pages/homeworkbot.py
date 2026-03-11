import streamlit as st
from helper import *

st.title("בוט שיעורי בית")
st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon='📖'
)

api_key = loadAPIKey()

showMessage("AI","היי אני כאן כדאי לעזור לך")

user = st.chat_input("...ההודעה שלך")

if user:
    showMessage("user",user)