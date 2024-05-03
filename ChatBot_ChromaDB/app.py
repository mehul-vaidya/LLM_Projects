#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py
#******************************************************************************************************
import pdf_loader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA 
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import HumanMessage , AIMessage
from typing import List
from langchain.schema import Document
import os
import streamlit as st
from dotenv import load_dotenv

#******************************************************************************************************
load_dotenv() 
persist_directory = "db"

#******************************************************************************************************
#streamlit used to create UI
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Citi Rewards")
st.title("Citi Rewards Credit Card Q&A Bot")    

#******************************************************************************************************t")    

class Genie:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.loader = TextLoader(self.file_path)
        self.documents = self.loader.load()
        self.texts = self.text_split(self.documents)
        self.vectordb = self.embeddings(self.texts)
        self.genie = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=os.environ["OPEN_API_KEY"], model_name="gpt-3.5-turbo"), chain_type="stuff", retriever=self.vectordb.as_retriever())

    @staticmethod
    def text_split(documents: TextLoader):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        return texts

    @staticmethod
    def embeddings(texts: List[Document]):
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])
        vectordb = Chroma.from_documents(texts, embeddings,persist_directory=persist_directory)
        vectordb.persist()
        return vectordb

    def ask(self, query: str):
        return self.genie.invoke(query).get('result')
#******************************************************************************************************

if __name__ == "__main__":
    pdf_loader.load_pdf("docs/Terms-and-Conditions.pdf")
    genie = Genie("result.txt")
    #print(genie.ask("What data is sent to the company? Can I get my money back as I don't like the service"))

    #conversation
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)        


    #ask questions
    user_query = st.chat_input("Your message")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            #ai_response =astra_vector_index.query(user_query,llm=llm).strip()   #get answer fromm LLM   
            #st.markdown(ai_response)   
            ai_response= genie.ask(user_query)  
            st.markdown(ai_response) 

        st.session_state.chat_history.append(AIMessage(ai_response)) 


 #******************************************************************************************************   