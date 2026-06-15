import os
from dotenv import load_dotenv
from google import genai
import streamlit as st
from helper import *



st.title("הצ'אט שלי")

st.set_page_config(
    page_title="שיחה עם צב נינג'ה",
    page_icon='🐢'
)

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_KEY = loadAPIKey()

gemini = genai.Client(api_key=API_KEY)


def saveToHistory(sender,text):
    st.session_state.history.append({
        "sender":sender,
        "text":text
    })

def send(promt):

    saveToHistory("user",promt)

    all_models = ["gemini-2.5-flash","gemini-2.0-flash","gemini-2.5-flash-lite","emini-2.0-flash-lite"]

    context = ""
    for line in st.session_state.history:
        context += f"{line['sender']}: {line['text']} \n"

    for model in all_models:
        chat = gemini.chats.create(model=model)
        try:
            message = chat.send_message(context)

            saveToHistory("assistant",message.text)

            return message
        except:
            print(f"לא עובד - מנסה את המודל הבא מודל{model}")

chat = gemini.chats.create(model="gemini-2.5-flash")

prompt = """
        אתה צב נינג'ה
        תענה ב10 מילים
        ענה על השאלה הבאה:
        מה שולמך?
"""

def start():
    st.session_state.gemini = genai.Client(api_key=API_KEY)
    st.session_state.history = []

    message = send(prompt)

    ai_msg = st.chat_message("assistant")
    ai_msg.write(message.text)

if "gemini" not in st.session_state:
    start()

if 'history' in st.session_state:
    for line in st.session_state.history[1:]:
        chat = st.chat_message(line["sender"])
        chat.write(line["text"])

promt = st.chat_input("Say something")
if promt:
    user_msg = st.chat_message("user")
    user_msg.write(promt)

    message = send(promt)
    ai_msg = st.chat_message("assistant")
    ai_msg.write(message.text)