from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_groq.chat_models import ChatGroq
from operator import itemgetter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import time
import streamlit as st
from openai import AuthenticationError

prompt = ChatPromptTemplate(
    messages=[
            SystemMessagePromptTemplate.from_template(
                """Answer all the questions the user asked to you.
                Question: {question}
                Helpful Answer:"""
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{question},")
        ],input_variables=["question"])


llm =  ChatGroq(
        api_key=st.secrets['GROQ_API_KEY'],
        model="llama3-70b-8192",
        temperature=0,
        max_retries=2,
        streaming=True
    )
memory = ConversationBufferWindowMemory(
        llm=llm, memory_key="history", return_messages=True,k=10)

def run_chatbot(user_question):
    try:
        chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(
                    memory.load_memory_variables) | itemgetter("history"),
            )
            | prompt
            | llm
        )
        output = ""
        for chunk in chain.stream({"question":user_question}):
            output += chunk.content
            yield chunk.content
            time.sleep(0.05)
        memory.save_context({"inputs": user_question}, {"output": output})
    except AuthenticationError:
        st.warning(
            body='AuthenticationError : Please provide correct api key 🔑' ,icon='🤖')
        return 'AuthenticationError'
