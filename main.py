import streamlit as st
from chat_response import run_chatbot

st.title('🦙💬 Llama 2 Chatbot')
st.sidebar.title('Models and Parameters')

st.markdown("""
<style>
     [data-testid=stSidebarUserContent]{
        background-color: grey;
            color: White;
    }
            
</style>
""", unsafe_allow_html=True)


temperature = st.sidebar.slider('Temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
top_p = st.sidebar.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
max_length = st.sidebar.slider('Max Length', min_value=32, max_value=500, value=120, step=8)


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
    
    
    slider_values = {
        'Temperature': temperature,
        'Top P': top_p,
        'Max Length': max_length
    }

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        result = run_chatbot(query,slider_values)
        response_text = result.get('text')
        full_response = ""
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})