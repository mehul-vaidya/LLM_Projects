#conda create -p venv python==3.9
#conda activate [venv]
#pip install -r requirements.txt
#need below libraby for running jupyter notebook
#pip install ipykernel 
#streamlit run app.py

'''
in this project we will read any given pdf
break it into chunks 
encode those chunks into vector
store vectors in DB
perform operation like search etc using those vectors

we use casendra db as db, which is hosted on https://astra.datastax.com/

model used is default open api model gpt-3.5-turbo-instruct
'''
#******************************************************************************************************
from langchain_community.vectorstores.cassandra  import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import cassio
#******************************************************************************************************
#to read PDF
from PyPDF2 import PdfReader
pdfreader = PdfReader('Terms-and-Conditions.pdf')

#from each page in pdf extract all text
from typing_extensions import Concatenate
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
#******************************************************************************************************

#initialize connection with db
#with cassio the engine powering the Astra DB integration in Langchain
#you wil also initialize the DB connection        
cassio.init(token=os.environ["AstraDB_TOEKN"],database_id=os.environ["AstraDB_ID"])

#create model
llm=OpenAI(openai_api_key=os.environ["OPEN_API_KEY"])
embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPEN_API_KEY"])

#create langchain vector store,
# we will store embedding we created by reading pdf into this db
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None
)

#*****************************************************************************************************
#store the data into vector db
#astra_vector_store.add_texts(texts[:50])
astra_vector_store.add_texts(texts[:50]) #you can limit this to avoid rate limit error on DB
astra_vector_index=VectorStoreIndexWrapper(vectorstore=astra_vector_store)
#******************************************************************************************************
#ask questions
first_question=True
counter=0

while True:
    query_text=input("\n Type question . q to quit\n").strip()
    if(query_text.lower()=="q"):
        break
    if(query_text=="") :
        continue

    answer=astra_vector_index.query(query_text,llm=llm).strip()
    print(answer)
    #print some other info
    #for doc, score in astra_vector_store.similarity_search_with_score(query_text,k=4):
    #    print("   [%0.4f] \"%s ... \"" % (score,doc.page_content[:84]))
        
