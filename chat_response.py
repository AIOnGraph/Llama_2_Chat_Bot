import streamlit as st
from langchain.llms.replicate import Replicate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate

memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=10,
        return_messages=True,
        input_key='question'
    )

replicate_api_token = st.secrets["REPLICATE_API_TOKEN"]

llm_model = "meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0"

prompt = ChatPromptTemplate(
    messages=[
            SystemMessagePromptTemplate.from_template(
                """Answer all the questions the user asked to you.
                Question: {question}
                Helpful Answer:"""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question},")
        ])

def run_chatbot(user_question,slider_values):
    print("Slider Values:", slider_values) 

    llm = Replicate(
    model=llm_model,
    streaming=False,
    replicate_api_token=replicate_api_token,
    model_kwargs=slider_values
)
    chains = LLMChain(memory=memory, prompt=prompt, llm=llm, verbose=True)
    
    result = chains({"question": user_question})
    return result
