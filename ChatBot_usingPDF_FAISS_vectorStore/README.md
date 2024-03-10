****
Difference between ChatBot_usingPDF project and ChatBot_usingPDF_FAISS_vectorStore is
in this project we have used FAISS vector store to store our pdf embeddings
FAISS vector store is part of langchain_community library itself.
****

In this project we have created chatbot which answers user's query about Citibank's credit card
we have used pdf file containing information about credit card as input 
we convert this file into small chunks and do embedding 
we then store these embedding into cassendra db hosted on datastax

we then take query from user , convert this query also in embedding
we then perform similarity check between pdf embedding and user query embedding with the help of openAI gpt-3.5-turbo-instruct
we then return most suitable response based on similarity score.

To run this code please follow below command
please create OPEN_API_KEY , AstraDB_TOEKN , AstraDB_ID and store it in .env file along with .py file
#conda create -p venv python==3.9
#conda activate [env name]
#pip install -r requirements.txt
#python app.py

This code take input from command line and produce output on command lime.
There is another code present in another repo , in which we have created UI using streamlit.

