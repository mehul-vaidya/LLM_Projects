#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py

'''
In this project we will find best state in given country
then we will find best city in state
we will find best restaurant and park in city
'''
#******************************************************************************************************
## Integrate our code OpenAI API
import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate 
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import SequentialChain
import streamlit as st

#------------------------------------------------------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
#------------------------------------------------------------------------------------------------------------------
st.title('Best restaurant Park Search')
input_text=st.text_input("Entry Country Name")
#------------------------------------------------------------------------------------------------------------------

state_prompt=PromptTemplate(
    input_variables=['country'],
    template="please give one of state in {country}"
)
city_name_prompt=PromptTemplate(
    input_variables=['state'],
    template="please give one of city in {state}"
)
restaurant_name_prompt=PromptTemplate(
    input_variables=['city'],
    template="what is best restaurant in {city}"
)
park_name_prompt=PromptTemplate(
    input_variables=['city'],
    template="what is best park in {city}"
)
#------------------------------------------------------------------------------------------------------------------
# Memory. store answers in langchain memory
state_memory = ConversationBufferMemory(input_key='country', memory_key='restaurant_park')
city_memory = ConversationBufferMemory(input_key='state', memory_key='restaurant_park')
restaurant_memory = ConversationBufferMemory(input_key='city', memory_key='restaurant_park')
park_memory = ConversationBufferMemory(input_key='city', memory_key='restaurant_park')
#------------------------------------------------------------------------------------------------------------------
## OPENAI LLMS
llm=OpenAI(openai_api_key=os.environ["OPEN_API_KEY"],model_name="gpt-3.5-turbo-instruct",temperature=0.5)
chain1=LLMChain(llm=llm,prompt=state_prompt,output_key='state',memory=state_memory)
chain2=LLMChain(llm=llm,prompt=city_name_prompt,output_key='city',memory=city_memory)
chain3=LLMChain(llm=llm,prompt=restaurant_name_prompt,output_key='restaurant',memory=restaurant_memory)
chain4=LLMChain(llm=llm,prompt=park_name_prompt,output_key='park',memory=park_memory)

#------------------------------------------------------------------------------------------------------------------

parent_chain=SequentialChain(chains=[chain1,chain2,chain3,chain4],input_variables=['country'],output_variables=['state','city','restaurant','park'],verbose=False)

if input_text:
    st.write(parent_chain({'country':input_text}))

    with st.expander('Best state'): 
        st.info(state_memory.buffer)

    with st.expander('Best city'): 
        st.info(city_memory.buffer)

    with st.expander('Best restaurant'): 
        st.info(restaurant_memory.buffer)

    with st.expander('Best park'): 
        st.info(park_memory.buffer)            

    