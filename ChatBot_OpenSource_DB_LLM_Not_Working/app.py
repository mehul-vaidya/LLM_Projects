#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py


'''
in this project we will read any given pdf. 
break it into chunks 
encode those chunks into vector
store vectors in DB
perform operation like search etc using those vectors

we use casendra db as db, which is hosted on https://astra.datastax.com/
'''
#******************************************************************************************************

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_core.messages import HumanMessage , AIMessage
from langchain.chains import RetrievalQA
import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
persist_directory = "db"

from langchain_community.llms import CTransformers

#******************************************************************************************************
#streamlit used to create UI
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Citi Rewards")
st.title("Citi Rewards Credit Card Q&A Bot")    

#******************************************************************************************************
#to read PDF
from PyPDF2 import PdfReader
pdfreader = PdfReader('Terms-and-Conditions.pdf')

#from each page in pdf extract all text
raw_text=""
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text+=content

#split pdf into chunks
from langchain.text_splitter import CharacterTextSplitter
text_spliter=CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len
)
texts=text_spliter.split_text(raw_text)  
texts=text_spliter.create_documents(texts)      

#******************************************************************************************************
#initialize connection with db
#with cassio the engine powering the Astra DB integration in Langchain
#you wil also initialize the DB connection        
#cassio.init(token=os.environ["AstraDB_TOEKN"],database_id=os.environ["AstraDB_ID"])

#create model

_="""
llm=CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin', model_type='llama',
                      config={'max_new_tokens':600,'temperature':0.01 , 'context_length': 1000})
"""
embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])
vectordb = Chroma.from_documents(texts, embedding,persist_directory=persist_directory)
vectordb.persist()

#use FAISS to store those embedding 
#document_search = FAISS.from_texts(texts, embedding)
#chain = load_qa_chain(llm, chain_type="stuff")

def getAnswer(query):
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=os.environ["OPEN_API_KEY"],model_name="gpt-3.5-turbo"), chain_type="stuff", retriever=vectordb.as_retriever())
    print("############" +query)
    qa.invoke(query).get('result')
    #docs = document_search.similarity_search(query)
    #return chain.run(input_documents=docs, question=query)

#create langchain vector store,
# we will store embedding we created by reading pdf into this db
_="""
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None
)
"""

#store the data into vector db
#astra_vector_store.add_texts(texts[:50])
#astra_vector_store.add_texts(texts[:30])#***************** side reduced to reduce rate limit error on DB
#astra_vector_index=VectorStoreIndexWrapper(vectorstore=astra_vector_store)
#******************************************************************************************************
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
        ai_response = getAnswer(user_query)   
        print("**************" + ai_response)
        st.markdown(ai_response)   

    st.session_state.chat_history.append(AIMessage(ai_response)) 

_="""
if prompt := st.chat_input("Type question. Type q to quit"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    answer=astra_vector_index.query(prompt,llm=llm).strip()   #get answer fromm LLM  
    with st.chat_message("assistant"):
        #response = st.write(answer)
        stream = llm.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

"""
#******************************************************************************************************

