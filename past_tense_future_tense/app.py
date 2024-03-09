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
st.title('Past Tense Future Tense')
input_text=st.text_input("Enter word")
#------------------------------------------------------------------------------------------------------------------
## OPENAI LLMS
llm=OpenAI(openai_api_key=os.environ["OPEN_API_KEY"],model_name="gpt-3.5-turbo-instruct",temperature=0.5)


#------------------------------------------------------------------------------------------------------------------
from langchain import PromptTemplate, FewShotPromptTemplate

# First, create the list of few shot examples.
examples_past = [
    {"present_tense": "awake", "past_tense": "awoke" },
    {"present_tense": "fall", "past_tense": "fell" },
]

examples_future = [
    {"present_tense": "awake" , "future_tense" : "awoken"},
    {"present_tense": "fall" , "future_tense" : "fallen"},
]

# Next, we specify the template to format the examples we have provided.
# We use the `PromptTemplate` class for this.
example_formatter_template_past = """
present tense: {present_tense}
past tense: {past_tense} 
"""

example_formatter_template_future = """
present tense: {present_tense}
future tense : {future_tense}
"""

example_prompt_past = PromptTemplate(
    input_variables=["present_tense", "past_tense"],
    template=example_formatter_template_past,
)

example_prompt_future = PromptTemplate(
    input_variables=["present_tense","future_tense"],
    template=example_formatter_template_future,
)
#------------------------------------------------------------------------------------------------------------------

# Finally, we create the `FewShotPromptTemplate` object.
few_shot_prompt_past = FewShotPromptTemplate(
    # These are the examples we want to insert into the prompt.
    examples=examples_past,
    # This is how we want to format the examples when we insert them into the prompt.
    example_prompt=example_prompt_past,
    # The prefix is some text that goes before the examples in the prompt.
    # Usually, this consists of intructions.
    prefix="Give the past tense every input\n",
    # The suffix is some text that goes after the examples in the prompt.
    # Usually, this is where the user input will go
    suffix="Word: {input}\n Past Tense : ",
    # The input variables are the variables that the overall prompt expects.
    input_variables=["input"],
    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
    example_separator="\n",
)

few_shot_prompt_future = FewShotPromptTemplate(
    # These are the examples we want to insert into the prompt.
    examples=examples_future,
    # This is how we want to format the examples when we insert them into the prompt.
    example_prompt=example_prompt_future,
    # The prefix is some text that goes before the examples in the prompt.
    # Usually, this consists of intructions.
    prefix="Give the future tense every input\n",
    # The suffix is some text that goes after the examples in the prompt.
    # Usually, this is where the user input will go
    suffix="Word: {input}\n Future Tense: ",
    # The input variables are the variables that the overall prompt expects.
    input_variables=["input"],
    # The example_separator is the string we will use to join the prefix, examples, and suffix together with.
    example_separator="\n",
)
#------------------------------------------------------------------------------------------------------------------

chain_past=LLMChain(llm=llm,prompt=few_shot_prompt_past)
chain_future=LLMChain(llm=llm,prompt=few_shot_prompt_future)

if input_text:
    _="""
    st.write(chain_past({'input':input_text}))
    st.write(chain_future({'input':input_text}))
    """
    with st.expander('Past Tense'): 
        st.info(chain_past({'input':input_text}))

    with st.expander('Future Tense'): 
        st.info(chain_future({'input':input_text}))    

    