#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py

import streamlit as st
from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain_community.chat_models import ChatOpenAI


from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

st.set_page_config(page_title="Chatbot")
st.header("Chatbot")

chat=ChatOpenAI(temperature=0.5,openai_api_key=os.environ["OPEN_API_KEY"])

if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]

def get_chatmodel_response(question):
    st.session_state['chat_history'].append(HumanMessage(content=question))
    answer=chat(st.session_state['chat_history']) ##this is most important step. we are passing entire chat history
    st.session_state['chat_history'].append(AIMessage(content=answer.content))
    return answer.content

input=st.text_input("Enter a message: ",key="input")
response=get_chatmodel_response(input)

submit=st.button("Ask the question")

if submit:
    st.subheader("The Response is")
    st.write(response)