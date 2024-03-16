#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

def getRespose(input_text,no_words):
    llm=CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin', model_type='llama',
                      config={'max_new_tokens':256,'temperature':0.1})
    
    template="""Write a travel blog for place {input_text} within {no_words} words."""
    prompt=PromptTemplate(input_variables=["input_text",'no_words'],template=template)
    response=llm(prompt.format(input_text=input_text,no_words=no_words))
    print(response)
    return response


st.set_page_config(page_title="Generate Travel Blogs",layout='centered',initial_sidebar_state='collapsed')
st.header("Generate Travel Blogs ")
input_text=st.text_input("Enter Name of Place for generating travel blog for it")
col1,col2=st.columns([5,5])

with col1:
    no_words=st.text_input('No of Words')
    
submit=st.button("Generate")

if submit:
    st.write(getRespose(input_text,no_words))