import streamlit as st
from helper import *
import PIL.Image


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
    אם אתה לא יודע - תחפש בגוגל
    **אל תמציא תשובה**
    ענה כמו בן אדם - בצורה אנושית
    
    **אם השתמשת בכלי (Tool) תכתוב את התוצאה**
    **אנחנו בשנת 2026**
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

image_button = st.file_uploader("העלאת תמונה", type=["png","jpg","jpeg"])

if user:
    showMessage("user",user)

    image = None

    if image_button:
        image = PIL.Image.open(image_button)

    save_to_history("homework","user",user)
    history = st.session_state["homework"]["history"]
    print(history)
    answer = sendMassage(user,system_prompt,history, image)

    showMessage("ai",answer)

    save_to_history("homework","model",answer)
