import streamlit as st
from helper import *

st.title("בוט שיעורי בית")
st.set_page_config(
    page_title="בוט שיעורי בית",
    page_icon='📖'
)

api_key = loadAPIKey()

showMessage("AI","היי אני כאן כדאי לעזור לך")

if "homework" not in st.session_state:
    newPage("homework")

system_prompt = """
    #תפקיד
    אתה בוט שיעורי בית
    #משימה
    המשימה שלך - לעזור לי בשיעורי בית
    תסביר ברור
    תכוון אותי לתשובה הנכונה
    #מגבלות
    אם אתה לא יודע - תגיד שאתה לא יודע
    **אל תמציא תשובה**
    ענה כמו בן אדם - בצורה אנושית
"""

st.session_state["homework"]["system_prompt"] = system_prompt

history = st.session_state["homework"]["history"]
for line in history:
    sender = line["role"]
    if sender == "model":
        sender = "ai"

    text = line["parts"][0]["text"]
    showMessage(sender,text)

user = st.chat_input("...ההודעה שלך")

if user:
    showMessage("user",user)
    save_to_history("homework","user",user)
    history = st.session_state["homework"]["history"]
    print(history)
    answer = sendMassage(user,system_prompt,history)

    showMessage("ai",answer)

    save_to_history("homework","model",answer)
