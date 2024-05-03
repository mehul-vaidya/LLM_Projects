This repo contains serveral small projects implemented using langchain , streamlit. 
such as chatbot , best restaurant & park finder , past and future tense of word app.
Refer readme in individual project

QA_ChatBot -> chatbot with direct query to LLM
QA_ChatBot_remember_History -> chatbot with direct query to LLM, but it remembers previous chat history

ChatBot_usingPDF_cmd -> chatbot which answers query on pdf document, works on command line. used casandra vector db
ChatBot_usingPDF-> chatbot which answers query on pdf document. has streamlit ui. used casandra vector db
ChatBot_usingPDF_FAISS_vectorStore -> chatbot which answers query on pdf document. has streamlit ui. used langchain internal FAISS vector db

Best_Restaurant_Park_Search-> given country , it find state, city . it then find best restaurant and park in city. used langchian prompts
Past_tense_future_tense -> given work , get past tense and future tense of work. used langchian prompts and FewShotLearning
Blog_generation_LLAMA_2 -> given location , generate travel blog

Voice_Generation-> text to voice generator using openAI api
Image_Generation-> text to Image generator using openAI api
Handwritten_Text_Extractor -> extract text from multi language invoice

ChatBot_ChromaDB -> we have used Chroma DB running on local machine to store vector embeddings
ChatBot_OpenSource_DB_LLM -> same as above but much simplified code

https://www.reddit.com/r/ChatGPTCoding/comments/14112ol/open_source_vector_databases/


