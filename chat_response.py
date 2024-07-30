from langchain_groq.chat_models import ChatGroq
import time
import streamlit as st
from openai import AuthenticationError



llm =  ChatGroq(
        api_key=st.secrets['GROQ_API_KEY'],
        model="llama3-70b-8192",
        temperature=0,
        max_retries=2,
        streaming=True
    )

def run_chatbot(user_question,prompt,memory):
    try:
        chain = ( prompt | llm )
        output = ""
        for chunk in chain.stream({"question":user_question,"memory":memory}):
            output += chunk.content
            yield chunk.content
            time.sleep(0.05)
    except AuthenticationError:
        st.warning(
            body='AuthenticationError : Please provide correct api key 🔑' ,icon='🤖')
        return 'AuthenticationError'
