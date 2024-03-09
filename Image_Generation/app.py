#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py

'''
generate image using dall-e-3
'''
#******************************************************************************************************
import os
import openai
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from openai import OpenAI
import streamlit as st
client = OpenAI(api_key=os.environ["OPEN_API_KEY"])
#******************************************************************************************************
st.set_page_config(page_title="Text to Image generation")
st.header("Text to Image generation")
#******************************************************************************************************
def generateImage(text):
  response = client.images.generate(
    model="dall-e-2",
    prompt=text,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  return response.data[0].url
#******************************************************************************************************

input=st.text_input("Input: ",key="input")
submit=st.button("Generate Image")

if submit:
    response=generateImage(input)
    st.subheader("Image generated")
    st.markdown('![Alt Text]({0})'.format(response))