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
#streamlit run app.py

This code take input and produce output using UI created U using streamlit.

