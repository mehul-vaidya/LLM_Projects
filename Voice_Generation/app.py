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
from pathlib import Path
import base64
import time
client = OpenAI(api_key=os.environ["OPEN_API_KEY"])
#******************************************************************************************************
st.set_page_config(page_title="Text to Audio generation")
st.header("Text to Audio generation")
speech_file_path = Path(__file__).parent / "speech.mp3"
#******************************************************************************************************
def generateAudio(text):
  response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=text
  )
  response.stream_to_file(speech_file_path)

#******************************************************************************************************
input=st.text_input("Input: ",key="input")
submit=st.button("Generate Audio")
#******************************************************************************************************
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
#******************************************************************************************************
if submit:
    generateAudio(input)
    st.write("# Auto-playing Audio!")
    st.subheader("Voice generated")
    autoplay_audio("speech.mp3")
    
    