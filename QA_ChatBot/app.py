#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py

# Q&A Chatbot
from langchain_openai import OpenAI

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os


## Function to load OpenAI model and get respones

def get_openai_response(question):
    llm=OpenAI(openai_api_key=os.environ["OPEN_API_KEY"],model_name="gpt-3.5-turbo-instruct",temperature=0.5)
    try:
        response=llm(question)
    except Exception as error:
        print("exception occured " + error)   
    return response

##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Langchain Application")

input=st.text_input("Input: ",key="input")
response=get_openai_response(input)

submit=st.button("Ask the question")

## If ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)