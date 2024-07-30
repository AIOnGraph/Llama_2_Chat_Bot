import streamlit as st
from chat_response import run_chatbot

st.title('🦙💬 Llama 2 Chatbot')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "Hi human!,How can I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if query := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        st.session_state.messages.append({"role": "assistant", "content": st.write_stream(run_chatbot(query))})