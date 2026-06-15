import streamlit as st
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import time
from ddgs import DDGS

def web_search(query : str) -> []:
    print("search: "+ query)

    with st.status("serch: "+ query):
        with DDGS() as d:
            results = d.text(query,region="he-il", max_results=3)
            return results

def current_time() -> str:
    """

    :return:
    """
    return time.ctime()

# --- קודם מגדירים את הפונקציה loadAPIKey ---
def loadAPIKey():
    load_dotenv()
    API_KEY = os.getenv("API_KEY") or st.secrets["API_KEY"]
    return API_KEY

# רשימת כל המודלים
all_models = [
    "gemini-3.5-flash",        # המודל המוביל כיום: מהיר, חכם ובעל יכולות מתקדמות
    "gemini-3.1-flash-lite",   # הגרסה החסכונית והמהירה ביותר למשימות בנפח גבוה
    "gemini-2.5-flash",        # מודל יציב מהדור הקודם (לגיבוי)
    "gemini-2.5-flash-lite"    # גרסת לייט מהדור הקודם (לגיבוי)
]

# יצירת Client אם הוא לא קיים
def createClient():
    st.session_state.client = genai.Client(api_key=loadAPIKey())

# שליחת הודעה לכל המודלים
def sendMassage(text,system_prompt,history=[],image=None):
    if 'client' not in st.session_state:
        createClient()

    content = [text]
    if image:
        content.append(image)
    for model in all_models:
        client = st.session_state.client
        try:
            chat = client.chats.create(
                model=model,
                history=history,
                config = types.GenerateContentConfig(
                    system_instruction = system_prompt,
                    tools = [current_time],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
                )
            )
            ai = chat.send_message(content)
            return ai.text

        except Exception as e:
            error = str(e)
            print(e)
            if "429" in error:
                st.error("שלחת יותר מידי הודעות, בבקשה לנסות מחר")
                return
            if "503" in error:
                st.info(f"מודל עמוס, ננסה מודל אחר")
            else:
                st.info("Error: " + error)
                return
            print(f"{model} not working...")


# הצגת הודעה בצ'אט של Streamlit
def showMessage(sender, text):
    newMessage = st.chat_message(sender)
    newMessage.write(text)

def save_to_history(project,sender,text):
    if project not in st.session_state:
        st.session_state[project] = {
            "history": []
        }
    st.session_state[project]["history"].append(
        {
            "role" : sender,
            "parts" : [{"text" : text}]
        }
    )

def newPage(project):
    st.session_state[project] = {
        "history": []
    }